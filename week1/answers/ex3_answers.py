"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
warning: `VIRTUAL_ENV=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
2026-04-13 23:53:24 INFO     rasa.tracing.backend_tracing_config  - [info     ] No backend tracing configuration found in endpoints.yml. Supported backend tracing types are 'jaeger' and 'otlp'. Backend tracing will not be configured. event_key=endpoint.read.no_backend_tracing_config filename=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/endpoints.yml
2026-04-13 23:53:26 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-13 23:53:28 INFO     rasa.core.processor  - [info     ] Loading model.                 event_key=rasa.core.processor.load_model model_path=models/20260413-235241-adjacent-cycle.tar.gz
2026-04-13 23:53:28 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/rasa/shared/utils/configs.py:53: FutureWarning: None: 'max_tokens' is deprecated and will be removed in 4.0.0. Use 'max_completion_tokens' instead.
  raise_deprecation_warning(
2026-04-13 23:53:28 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-13 23:53:28 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-13 23:53:28 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-13 23:53:28 INFO     faiss.loader  - Loading faiss with AVX2 support.
2026-04-13 23:53:29 INFO     faiss.loader  - Successfully loaded faiss with AVX2 support.
2026-04-13 23:53:29 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
2026-04-13 23:53:29 WARNING  rasa.validator  - [warning  ] Default pattern flows include responses with rephrasing enabled, but the NLG endpoint is not configured in endpoints.yml. Rephrasing for default patterns will be skipped. event_key=validator.verify_rephrase_endpoints_consistency.defaults_only_rephrase_without_nlg
2026-04-13 23:53:29 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                   
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                            
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                            
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                   
2026-04-13 23:55:46 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is confirming a booking, and the conversation history shows they\'ve already provided the guest count (160) and the number of vegan meals (50). Now the user says "£200 deposit". The AI\'s last question was about the deposit amount in GBP.

The current active flow is confirm_booking, and the requested slot is deposit_amount_gbp. The user is providing the deposit amount here. So I need to set the deposit_amount_gbp slot to 200. Since the user mentioned £200, the value should be 200.0 as per the slot\'s float type. 

I should check if there are any other slots needed in the confirm_booking flow. The slots listed are guest_count, vegan_count, and deposit_amount_gbp. All of these have been filled except deposit_amount_gbp, which the user just provided. Once this is set, the flow can proceed. There\'s no ambiguity here, so no need for disambiguate. The user hasn\'t mentioned anything outside the booking confirmation, so no need to start another flow. The action should be to set the deposit amount and then start the confirm_booking flow if it\'s not already active. Wait, the current active flow is already confirm_booking, so maybe just setting the slot is needed. But the example in the instructions shows that when a user provides a value, you set the slot and start the flow. Wait, in the first example, when the user says "send money to John", the output includes both set slot and start flow. But in the current state, the flow is already active. So maybe in this case, since the flow is already active, we just set the slot. But maybe after setting the slot, we need to start the flow again? Or perhaps the flow is already running, and setting the slot is sufficient. Let me check the instructions again.

The instructions say: "start flow transfer_money" when the user mentions the action. But in this case, the flow is already active. So perhaps the correct action here is just to set the slot. However, looking at the example where the user says "set up a recurrent payment", the output includes start flow and set slots. But in that case, the flow wasn\'t active yet. Since the current flow is already confirm_booking, maybe we don\'t need to start it again. So the action here is to set the deposit_amount_gbp to 200.0.' message='No commands were parsed from the LLM actions.'
2026-04-13 23:55:46 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200                                                                                                                            
2026-04-13 23:56:12 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is in the confirm_booking flow. The current step is asking for the deposit_amount_gbp. The user previously said "£200 deposit", but the AI didn\'t understand. Then the AI asked again, and the user just said "200". 

So, the user is providing the deposit amount. The slot is deposit_amount_gbp, which is a float. The user\'s response is "200", which is a number. I need to set that slot with 200.0, maybe as a float. Since the user already provided the necessary info, and there\'s no ambiguity, the action should be to set the slot and maybe complete the flow.

Wait, the current state shows that guest_count and vegan_count are already filled. The only missing slot is deposit_amount_gbp. Once this is set, the flow can be completed. So the actions would be to set the deposit amount and then start the confirm_booking flow? Or is the flow already active? The active_flow is confirm_booking, so maybe after setting the slot, the flow is completed. But the available actions don\'t include completing a flow. The options are start, cancel, disambiguate, etc. Hmm.

Wait, the instructions say to start a flow when appropriate. Since the user has provided all required slots, maybe the flow is done. But the AI\'s job is to process the input. Since the user answered the last question, the AI might need to confirm and end the flow. But the available actions don\'t have an end flow. So perhaps after setting the slot, the flow is completed implicitly. The action list should include setting the slot and then starting the confirm_booking flow again? Or maybe just setting the slot is enough. Wait, the flow is already active. The AI\'s next step would be to process the slot and then proceed. Since all slots are filled, maybe the flow is done. But the action list should only include the necessary actions based on the user\'s input.

The user\'s last message is "200", which is the deposit amount. So the action is to set deposit_amount_gbp to 200.0. Then, since all slots are filled, maybe the flow is completed, but the AI doesn\'t need to start another flow. So the only action is set slot deposit_amount_gbp 200.0. But the example in the slot extraction shows that when a slot is set, you also' message='No commands were parsed from the LLM actions.'
2026-04-13 23:56:12 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200                                                                                                                            
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
cd exercise3_rasa && uv run rasa shell
warning: `VIRTUAL_ENV=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
2026-04-13 23:58:36 INFO     rasa.tracing.backend_tracing_config  - [info     ] No backend tracing configuration found in endpoints.yml. Supported backend tracing types are 'jaeger' and 'otlp'. Backend tracing will not be configured. event_key=endpoint.read.no_backend_tracing_config filename=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/endpoints.yml
2026-04-13 23:58:38 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-13 23:58:38 INFO     rasa.core.processor  - [info     ] Loading model.                 event_key=rasa.core.processor.load_model model_path=models/20260413-235241-adjacent-cycle.tar.gz
2026-04-13 23:58:39 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/rasa/shared/utils/configs.py:53: FutureWarning: None: 'max_tokens' is deprecated and will be removed in 4.0.0. Use 'max_completion_tokens' instead.
  raise_deprecation_warning(
2026-04-13 23:58:39 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-13 23:58:39 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-13 23:58:39 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-13 23:58:39 INFO     faiss.loader  - Loading faiss with AVX2 support.
2026-04-13 23:58:39 INFO     faiss.loader  - Successfully loaded faiss with AVX2 support.
2026-04-13 23:58:39 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
2026-04-13 23:58:39 WARNING  rasa.validator  - [warning  ] Default pattern flows include responses with rephrasing enabled, but the NLG endpoint is not configured in endpoints.yml. Rephrasing for default patterns will be skipped. event_key=validator.verify_rephrase_endpoints_consistency.defaults_only_rephrase_without_nlg
2026-04-13 23:58:39 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                   

How many guests are you confirming for tonight's event?
Your input ->  calling to confirm a booking                                                                                                   

How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                            

2026-04-13 23:59:43 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user\'s last message is "160". The current flow is confirm_booking, and the active step is asking for guest_count. The AI previously asked how many guests are confirming for tonight\'s event, and the user responded with 160.

So, the first action should be to set the guest_count slot to 160. Since the slot is of type float, but the user provided an integer, I can still set it as 160.0 if needed, but the example shows using the exact value. The instructions say to extract text exactly as provided, so probably just 160.

Then, after setting the slot, the next step would be to ask for the next required slot. The remaining slots are vegan_count and deposit_amount_gbp. The AI needs to prompt the user for one of these. The next step in the flow would be to ask for vegan_count. So the action would be to start the next step in the confirm_booking flow, asking for vegan_count. But looking at the available actions, there\'s no "ask for next slot" action. Wait, the available actions are start flow, set slot, etc. The AI\'s response would be to ask the user for the next required slot. Since the current flow is confirm_booking, and the next requested slot is vegan_count, the AI should ask the user for that. But how to represent that in the action list? The available actions don\'t include a "ask" action. Wait, the actions are things like start flow, set slot, provide info, etc. So after setting the guest_count, the AI should proceed to the next step in the flow, which would be to ask for vegan_count. But how is that handled? The example in the slot extraction shows that when a user provides a value, the AI sets the slot and then starts the flow. Wait, no. The example shows that when the user says "send money to John", the output includes set slot and start flow. But in this case, the flow is already started (confirm_booking is the active flow). So after setting the guest_count, the AI should move to the next step in the flow, which would be to ask for vegan_count. But the available actions don\'t have a way to indicate moving to the next step. Wait, maybe the AI is supposed to generate a message asking for the next slot, but the action list here is about the actions to take, not the message.' message='No commands were parsed from the LLM actions.'
2026-04-13 23:59:43 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                            

And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                             
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  500                                                                                                                            
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "Agent informed that deposit chosen (£500) exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
cd exercise3_rasa && uv run rasa shell
warning: `VIRTUAL_ENV=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
2026-04-14 00:06:00 INFO     rasa.tracing.backend_tracing_config  - [info     ] No backend tracing configuration found in endpoints.yml. Supported backend tracing types are 'jaeger' and 'otlp'. Backend tracing will not be configured. event_key=endpoint.read.no_backend_tracing_config filename=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/endpoints.yml
2026-04-14 00:06:02 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-14 00:06:03 INFO     rasa.core.processor  - [info     ] Loading model.                 event_key=rasa.core.processor.load_model model_path=models/20260413-235241-adjacent-cycle.tar.gz
2026-04-14 00:06:03 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/rasa/shared/utils/configs.py:53: FutureWarning: None: 'max_tokens' is deprecated and will be removed in 4.0.0. Use 'max_completion_tokens' instead.
  raise_deprecation_warning(
2026-04-14 00:06:03 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-14 00:06:03 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-14 00:06:03 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-14 00:06:03 INFO     faiss.loader  - Loading faiss with AVX2 support.
2026-04-14 00:06:03 INFO     faiss.loader  - Successfully loaded faiss with AVX2 support.
2026-04-14 00:06:03 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
2026-04-14 00:06:03 WARNING  rasa.validator  - [warning  ] Default pattern flows include responses with rephrasing enabled, but the NLG endpoint is not configured in endpoints.yml. Rephrasing for default patterns will be skipped. event_key=validator.verify_rephrase_endpoints_consistency.defaults_only_rephrase_without_nlg
2026-04-14 00:06:03 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                   
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                            
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?                                                                                      
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
It answered back that it can only help with confirming tonight venue booking and for anything else contact the event organizer directly."""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
When I compared the two agents, I found the LangGraph agent noticeably friendlier than the Rasa agent. It came across as more empathetic because it explained why it could not answer, mentioned that it did not have the required capability, and also shared what it could still help with. That made it feel like an agent I would be more willing to interact with again. In contrast, the Rasa agent was much more direct. It simply stated that it could not help, told me to contact the organizer, and referred to the rule. From a customer experience perspective, that felt colder and somewhat rude.
At the same time, from a security perspective, I felt the opposite. The LangGraph agent seemed to reveal too much by mentioning its tools and exposing details about how the system was configured behind the scenes. That makes it feel less secure, because it gives away internal information that a user does not need. The Rasa agent, although less warm, felt safer because it focused only on the rule and the outcome without revealing anything about the underlying system.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
warning: `VIRTUAL_ENV=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
2026-04-14 00:29:10 INFO     rasa.tracing.backend_tracing_config  - [info     ] No backend tracing configuration found in endpoints.yml. Supported backend tracing types are 'jaeger' and 'otlp'. Backend tracing will not be configured. event_key=endpoint.read.no_backend_tracing_config filename=/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/endpoints.yml
2026-04-14 00:29:11 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-14 00:29:12 INFO     rasa.core.processor  - [info     ] Loading model.                 event_key=rasa.core.processor.load_model model_path=models/20260414-002830-unsolvable-union.tar.gz
2026-04-14 00:29:12 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
/Users/sahanavenkatesh/nebius/lesson_1_ai_agents/assignment1/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/rasa/shared/utils/configs.py:53: FutureWarning: None: 'max_tokens' is deprecated and will be removed in 4.0.0. Use 'max_completion_tokens' instead.
  raise_deprecation_warning(
2026-04-14 00:29:12 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-14 00:29:12 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-14 00:29:12 WARNING  rasa.shared.utils.llm  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-14 00:29:12 INFO     faiss.loader  - Loading faiss with AVX2 support.
2026-04-14 00:29:13 INFO     faiss.loader  - Successfully loaded faiss with AVX2 support.
2026-04-14 00:29:13 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating   
2026-04-14 00:29:13 WARNING  rasa.validator  - [warning  ] Default pattern flows include responses with rephrasing enabled, but the NLG endpoint is not configured in endpoints.yml. Rephrasing for default patterns will be skipped. event_key=validator.verify_rephrase_endpoints_consistency.defaults_only_rephrase_without_nlg
2026-04-14 00:29:13 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->   calling to confirm a booking                                                                                                  

How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                     

2026-04-14 00:29:58 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user called to confirm a booking, and the AI asked for the number of guests. The user responded with "160 guests". 

First, I need to check the active flow. The current flow is confirm_booking, and the requested slot is guest_count. The user provided 160, which is a number. The slot for guest_count is of type float, so I should set that slot to 160.0.

Since the user answered the question, the next step would be to move to the next requested slot in the flow. But the current step only mentions guest_count as the requested slot. The other slots, vegan_count and deposit_amount_gbp, are still undefined. So the AI should probably ask for the next piece of information, which would be either vegan_count or deposit_amount_gbp. But according to the instructions, I should only process the user\'s last message. The user only provided guest_count, so I set that slot and then the flow continues. The next action would be to prompt for the next required slot. However, the current step in the active flow only has guest_count as the requested slot. Wait, maybe the flow is structured to ask one slot at a time. So after setting guest_count, the AI should proceed to ask for the next slot, which might be vegan_count. But the current state\'s current_step only has guest_count as the requested slot. Maybe the system is designed to handle each slot step by step. So after setting guest_count, the next step would be to ask for the next slot. But the user hasn\'t provided any other info yet. So the action here is to set the guest_count slot to 160.0 and then the system will handle the next step, which might be to ask for vegan_count or deposit_amount. But according to the instructions, I only need to output the actions based on the user\'s last message. So the correct action here is to set the guest_count slot with 160.0 and start the confirm_booking flow if it\'s not already active. Wait, the active flow is already confirm_booking, so no need to start it again. So the action is just setting the slot. Also, check if there\'s any other info in the user\'s message. The user said "160 guests", which directly answers the guest_count. No other slots mentioned. So the only action is to set the guest_count to 160.0.
</think>' message='No commands were parsed from the LLM actions.'
2026-04-14 00:29:58 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                     

And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                             

What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200                                                                                                                            
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
In the old Rasa, Python handled slot extraction via regex and intent classification via NLU training examples. CALM offloads both to the LLM, which means no regex maintenance and no retraining when phrasing changes.
Python still handles the £300 deposit limit check in ActionValidateBooking because that is a hard business rule where LLM interpretation would be unpredictable and potentially unsafe.
The old approach felt more auditable for slot extraction — a regex for guest_count is easy to reason about. The LLM extraction is more flexible but harder to test exhaustively.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The CALM agent cannot improvise outside the flows defined in flows.yml, and it cannot call a tool that was not declared there. LangGraph could reason freely and call any available tool dynamically. For a booking confirmation use case, this constraint is a feature, not a limitation. You do not want an agent that improvises pricing, invents new policies, or takes actions the business did not explicitly authorise. The setup cost of config files, training, and a Rasa Pro licence buys you a bounded, auditable agent whose behaviour is fully predictable.
"""
