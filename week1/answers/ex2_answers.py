"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability", "check_pub_availability","calculate_catering_cost","get_edinburgh_weather","generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = True

TASK_A_NOTES = "The agent confirmed both venues and calculated the catering cost for both."   # optional — anything unexpected

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True   # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://i.ibb.co/M58yZJ0Z/9a44e09ac481.png"
# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """The agent is unaware of how the image is generated. It just uses the tool to create the image. Tool is written in a safe way that protects it against live image generation failures. On error, it safely switches to placeholder.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The pivot moment was when The Bow Bar returned status "full" and the agent moved on to check other venues.

  [TOOL_CALL]    → check_pub_availability({"pub_name": "The Bow Bar", "required_capacity": 160, "requires_vegan": true})
  [TOOL_RESULT]  ← check_pub_availability: {"success": true, "pub_name": "The Bow Bar", "address": "80 West Bow, Edinburgh", "capacity": 80, "vegan": true, "status": "full", "meets_all_constraints": false}
  [TOOL_CALL]    → check_pub_availability({"pub_name": "The Haymarket Vaults", "required_capacity": 160, "requires_vegan":)
  [TOOL_RESULT]  ← check_pub_availability: {"success": true, "pub_name": "The Haymarket Vaults", "address": "1 Dalry Road, Edinburgh", "capacity": 160, "vegan": true, "status": "available", "meets_all_constraints": true}
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False   # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """Okay, let's see. The user asked for a venue that can hold 300 people with vegan options. I checked all four pubs using the check_pub_availability function. The results show that none of the pubs meet the capacity requirement. The Albanach has a capacity of 180, Haymarket Vaults 160, Guilford Arms 200, and Bow Bar 80. All are below 300. Even though The Albanach and Haymarket Vaults have vegan options, their capacities are too small. The Guilford Arms doesn't even have vegan options. The Bow Bar is full. So, none of the known venues can accommodate 300 people. The user might need to look for a larger venue or consider multiple locations. I should inform them that the current options don't meet the requirements and suggest alternatives.\n</think>\n\nNone of the known Edinburgh venues can accommodate 300 people while meeting all requirements. The maximum capacities are:\n- The Albanach: 180 (vegan available)\n- Haymarket Vaults: 160 (vegan available)\n- Guilford Arms: 200 (no vegan)\n- Bow Bar: 80 (vegan available, currently full)\n\nWould you like to:\n1. Consider combining multiple venues?\n2. Explore non-listed venues with higher capacity?\n3. Adjust the guest count or dietary requirements?
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = """Okay, the user is asking about the last train time from Edinburgh Waverley to London tonight. Let me check the tools provided.\n\nLooking at the available functions: check_pub_availability, get_edinburgh_weather, calculate_catering_cost, generate_event_flyer. None of these are related to train schedules. The functions are for checking pub availability, weather, catering costs, and generating flyers. \n\nSince there's no tool for train times, I can't use any of the provided functions to answer this. I need to inform the user that I don't have access to that information and suggest they check a train service website or app.\n</think>\n\nI don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:\n1. The National Rail website (https://www.nationalrail.co.uk)\n2. Train service apps like Citymapper or Trainline\n3. The specific train operator's website (e.g., LNER)\n\nWould you like help with anything related to Edinburgh pubs, weather, or event planning instead?"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """I think the answer is acceptable because the agent did not make up a venue. I liked that the agent explained what it can do and why it could not help. It also suggested resources the user can look at.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
LangGraph is better suited for handling out-of-scope questions and unexpected failures than RASA. RASA is more deterministic in the sense that we can predict its failures more easily.
The agent code can be reused across tasks, whereas the YAML format does not lend itself as much to reusability in its current form.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The generated image had spelling errors, which was unexpected for a professional flyer.
When asked an out-of-scope question, the agent did not call a tool and it correctly informed the user that the question was out of scope and explained what it is designed to help with.
"""
