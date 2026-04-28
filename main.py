import json
from pathlib import Path
from deepagents import create_deep_agent
from tools import get_weather, get_person_info, get_trip_plan, get_tool_by_name

manager_context=""
with open("manager.md","r") as f:
    manager_context = f.read()

agent_dictionary={}

with open("agents.json", 'r') as f:
    agent_dictionary = json.load(f)

subagents=[]

for entry in agent_dictionary:
    if not isinstance(entry, dict):
        raise ValueError("Each agent registry entry must be an object")

    name = str(entry.get("name", "")).strip()
    prompt_file_path = str(entry.get("skills", "")).strip()
    # available_tools = entry.get("available_tools") or []
    available_tools = [get_tool_by_name(val) for val in entry.get("tools", [])]

    if not name:
        raise ValueError("Agent registry entry missing name")
    if not prompt_file_path:
        raise ValueError(f"Agent registry entry missing prompt_file for {name}")
    if not isinstance(available_tools, list):
        raise ValueError(f"available_tools must be a list for {name}")

    system_prompt = Path(prompt_file_path).read_text(encoding="utf-8")

    subagents.append({
        "name": name,
        "description": f"Friendly agent: {name}. Follow this guide in every response:\n{system_prompt}",
        "system_prompt": f"{system_prompt}",
        "tools": available_tools,
    })


agent = create_deep_agent(
    model="gpt-4o-mini",
    system_prompt=manager_context,
    tools=[get_weather, get_person_info, get_trip_plan]
)

result = agent.invoke({"messages": [{"role":"user","content":"Plan a trip for me to Delhi?"}]},)

print("Result: ", result, "\n")

for i, val in enumerate(result["messages"]):
    print("Agent Response ", i, val.content, "\n")


# import json
# from pathlib import Path
# from langgraph.types import Command
# from deepagents import create_deep_agent
# from langchain_core.utils.uuid import uuid7
# from tools import get_tool_by_name, TOOL_REGISTRY
# from langgraph.checkpoint.memory import MemorySaver

# agent_dictionary={}

# with open("agents.json", 'r') as f:
#     agent_dictionary = json.load(f)

# subagents=[]

# for entry in agent_dictionary:
#     if not isinstance(entry, dict):
#         raise ValueError("Each agent registry entry must be an object")

#     name = str(entry.get("name", "")).strip()
#     prompt_file_path = str(entry.get("skills", "")).strip()
#     # available_tools = entry.get("available_tools") or []
#     available_tools = [get_tool_by_name(val) for val in entry.get("tools", [])]

#     if not name:
#         raise ValueError("Agent registry entry missing name")
#     if not prompt_file_path:
#         raise ValueError(f"Agent registry entry missing prompt_file for {name}")
#     if not isinstance(available_tools, list):
#         raise ValueError(f"available_tools must be a list for {name}")

#     system_prompt = Path(prompt_file_path).read_text(encoding="utf-8")

#     subagents.append({
#         "name": name,
#         "description": f"Fraud specialist: {name}. Follow this guide in every response:\n{system_prompt}",
#         "system_prompt": f"{system_prompt}",
#         "tools": available_tools,
#     })

# manager_context=""
# with open("manager.md","r") as f:
#     manager_context = f.read()

# agent = create_deep_agent(
#     system_prompt=manager_context,
#     model="gpt-4o-mini",
#     subagents=subagents,
# )
# print("Script Started...")

# result = agent.invoke({"messages": [{"role":"user","content":"What is the weather of Delhi?"}]},)

# print("Result: ", result, "\n")

# for i, val in enumerate(result["messages"]):
#     print("Agent Response ", i, val.content, "\n")

