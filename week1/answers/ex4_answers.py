"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults."
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  =  "Okay, the user is looking for a venue in Edinburgh that can hold 300 people and has vegan options. I first tried using the search_venues function with min_capacity 300 and requires_vegan true, but got a validation error. Then I adjusted the call to include the parameters under the \"input\" object, which fixed the error. However, the response came back with zero matches.\n\nHmm, so there are no venues that meet both the capacity and vegan requirements. But maybe the user is okay with a venue that has a vegan option but isn't strictly required? Or perhaps they can adjust the capacity? Let me check the functions again. The search_venues function allows specifying min_capacity and requires_vegan. If there are no results, maybe I should consider lowering the min_capacity or checking if the vegan requirement is too strict.\n\nWait, the user specifically asked for vegan options, so maybe they can't compromise on that. In that case, there's no venue available. But I should present this clearly. Alternatively, maybe there's a mistake in the parameters. Let me confirm the function's parameters again. The function requires min_capacity as a number and requires_vegan as a boolean. The user's input was correct.\n\nSo the answer should inform the user that no venues meet the criteria. Maybe suggest adjusting the capacity or checking other options. But since the user's query was specific, I should state that there are no available venues with those requirements.\n</think>\n\nThere are currently no Edinburgh venues available that can accommodate 300 people with vegan options. Would you like to try adjusting the capacity requirements or checking for non-vegan venues?"

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
I needed to modify venue_server.py and change The Albanach's status to full. For the first query, it was able to confirm The Haymarket Vaults. The second query failed as there was no venue with the required capacity.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 156   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 57   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP involves much less code than working directly within the tool constraints, which is evident from the count above. That is because the integration layer between the model and the tool is already abstracted away, letting the author focus on the actual tool logic.

It is also more robust. Since each tool can run in its own environment, it is easier to manage different package versions and dependencies cleanly. In a conventional setup, everything often ends up tangled in one shared environment, which makes the system harder to manage and more fragile.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
     list of subgoals. It lives upstream of the ReAct loop in the
     autonomous-loop half of PyNanoClaw, so the Executor never sees an
     ambiguous task.
- The Executor is a weaker model which takes the subgoals produced by the Planner and executes them fast.
    It lives downstream of the ReAct loop in the autonomous-loop half of PyNanoClaw.
- The Memory store is a component that is shared between the autonomous loop and the structured agent. It stores episodes and general summaries across conversations.
- The Structured Agent is a simple agent with a reasoning model and rules to follow. This is to make sure we are following the core business logic.
- Tools / MCP servers for the Executor to execute the goals. They can range from simple Python functions to complicated queries.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
For research, an autonomous loop makes sense. Research needs a structure with clear goals, but it also needs room to branch out and explore different directions. It is hard to tightly constrain research, because some of the best insights come from following unexpected avenues. You can set basic boundaries, but the model should still have freedom to explore multiple paths and deepen its understanding of the topic.
For a call flow, I would use a more structured agent. In that setting, it is important for the model to follow clear and reliable logic. The agent should not expose its internal architecture, because that makes it more vulnerable to external attacks. It also needs to stick closely to the business logic, handle failures well, and remain robust under pressure.
In the train-related queries, the LangGraph agent referenced sources like National Rail even though those sources were not explicitly exposed as available tools. That made it feel more capable from a user experience standpoint, but it also raised concerns about how clearly it respected its actual tool boundaries. By contrast, the Rasa car agent handled the situation in a much more controlled way: it clearly stated that the request was outside its scope, directed the user to contact the event organizer, and did so without exposing anything about its internal setup.
"""