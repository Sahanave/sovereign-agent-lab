"""
sovereign_agent/agents/research_agent.py
=========================================
The Research Agent for your Sovereign Agent project.

This is the file that grows each week:

  Week 1 (now):    Basic ReAct loop with 4 venue tools
  Week 2:          Add real web search and file operation tools
  Week 3:          Split into Planner (DeepSeek R1) + Executor (Llama 70B)
  Week 4:          Add CLAUDE.md memory so the agent remembers past sessions
  Week 5:          Add observability, cost tracking, and safety guardrails

The public interface — run_research_agent(task, max_turns) → dict — stays the
same across all weeks. Week 2's code imports and calls this function exactly
as Week 1 leaves it. You add capability inside; the callers don't change.

HOW TO USE
----------
Import and call from exercise files:

    from sovereign_agent.agents.research_agent import run_research_agent

    result = run_research_agent(
        task="Find a pub for 160 vegan guests tonight.",
        max_turns=8,
    )
    print(result["final_answer"])
    print(result["tool_calls_made"])

ADDING TOOLS IN FUTURE WEEKS
-----------------------------
To add a new tool, import it and add it to the TOOLS list below.
The agent picks up the new capability automatically — no other changes needed.

    # Week 2 example:
    from sovereign_agent.tools.web_search import search_web
    TOOLS = [
        check_pub_availability,
        get_edinburgh_weather,
        calculate_catering_cost,
        generate_event_flyer,
        search_web,           # ← just add here
    ]
"""

import json
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent  # kept for task_d graph visualisation

from sovereign_agent.tools.venue_tools import (
    check_pub_availability,
    get_edinburgh_weather,
    calculate_catering_cost,
    generate_event_flyer,
)

load_dotenv()

# ─── Model ────────────────────────────────────────────────────────────────────
# Week 1: single model handles everything
# Week 3: this gets split into llm_planner (DeepSeek R1) and llm_executor (Llama 70B)

llm = ChatOpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0,
)

# ─── Tool registry ────────────────────────────────────────────────────────────
# Week 1: 4 venue tools
# Week 2: add search_web, read_file, write_file here

TOOLS = [
    check_pub_availability,
    get_edinburgh_weather,
    calculate_catering_cost,
    generate_event_flyer,
]

# Kept for task_d graph visualisation in exercise2_langgraph.py
_agent = create_react_agent(llm, TOOLS)


# ─── Text-based tool call parser ──────────────────────────────────────────────
# The Nebius TokenFactory endpoint with Llama 3.3-70B does not fully implement
# OpenAI's function-calling protocol.  Instead of returning tool calls in the
# structured `tool_calls` field, the model embeds them as a JSON array in the
# plain text content, with each element being a JSON-encoded dict:
#
#   ["{"type": "function", "name": "...", "parameters": {...}}", ...]
#
# LangGraph's create_react_agent only checks message.tool_calls, sees nothing,
# and immediately returns the JSON text as the "final answer".  This helper
# parses that text format so the custom loop below can execute the tools.

def _parse_text_tool_calls(content: str) -> list[dict]:
    """
    Parse Nebius/Llama text-based tool calls from a message content string.

    Returns a list of {"name": str, "args": dict} dicts, or [] if none found.
    """
    if not isinstance(content, str):
        return []
    content = content.strip()
    if not content.startswith("["):
        return []
    try:
        outer = json.loads(content)
        if not isinstance(outer, list):
            return []
        result = []
        for item in outer:
            # Each element may itself be a JSON-encoded string
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except Exception:
                    continue
            if not isinstance(item, dict):
                continue
            if item.get("type") == "function" and "name" in item:
                args = item.get("parameters", item.get("arguments", {}))
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                result.append({"name": item["name"], "args": args})
        return result
    except Exception:
        return []


# ─── Public interface ─────────────────────────────────────────────────────────

def run_research_agent(task: str, max_turns: int = 8) -> dict:
    """
    Run the research agent on a task and return a structured result.

    Args:
        task:      Natural language task description
        max_turns: Maximum number of reasoning turns before giving up

    Returns:
        dict with keys:
          final_answer:    str — the agent's final response
          tool_calls_made: list of dicts — each tool call with name and args
          full_trace:      list of dicts — every message in the conversation
          success:         bool — True if agent gave a final answer (not max_turns)

    This return shape is the contract that Week 2+ code will depend on.
    Do not change the key names.
    """
    llm_with_tools = llm.bind_tools(TOOLS)
    tool_map = {t.name: t for t in TOOLS}

    messages: list = [HumanMessage(content=task)]
    tool_calls_made: list = []
    full_trace: list = [{"role": "human", "content": task}]
    final_answer = ""

    for _ in range(max_turns):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # ── Collect tool calls: standard format first, text-based as fallback ─
        tc_list = list(getattr(response, "tool_calls", []) or [])
        is_text_based = False

        if not tc_list:
            parsed = _parse_text_tool_calls(response.content)
            if parsed:
                tc_list = [
                    {"name": t["name"], "args": t["args"], "id": f"text_{i}"}
                    for i, t in enumerate(parsed)
                ]
                is_text_based = True

        if not tc_list:
            # No tool calls — this is the final answer
            final_answer = str(response.content) if response.content else ""
            if final_answer:
                full_trace.append({"role": "ai", "content": final_answer})
            break

        # ── Execute each tool and collect results ──────────────────────────────
        tool_results = []
        for tc in tc_list:
            name = tc["name"]
            args = tc.get("args", {})

            tool_calls_made.append({"tool": name, "args": args})
            full_trace.append({"role": "tool_call", "tool": name, "args": args})

            tool_fn = tool_map.get(name)
            result = (
                tool_fn.invoke(args)
                if tool_fn
                else json.dumps({"success": False, "error": f"Unknown tool: {name}"})
            )
            full_trace.append({"role": "tool", "content": str(result)})
            tool_results.append((tc, str(result)))

        # ── Feed results back to the model ────────────────────────────────────
        if is_text_based:
            # Text-based calls: bundle all results into one human message
            combined = "\n".join(
                f"[{tc['name']} result]\n{result}"
                for tc, result in tool_results
            )
            messages.append(HumanMessage(
                content=f"Tool results:\n{combined}\n\nPlease provide your final answer."
            ))
        else:
            # Standard calls: one ToolMessage per call
            for tc, result in tool_results:
                messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tc["id"],
                ))

    return {
        "final_answer":    final_answer,
        "tool_calls_made": tool_calls_made,
        "full_trace":      full_trace,
        "success":         bool(final_answer),
    }
