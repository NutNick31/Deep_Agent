import json
from uuid import uuid4
from pathlib import Path
from fastapi import FastAPI
from tools import get_tool_by_name
from deepagents import create_deep_agent

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
    subagents=subagents
)

# result = agent.invoke({"messages": [{"role":"user","content":"I want to know that whether the operator UPPRD_KHERI_NS917529 is fraud or not"}]},)

# print("Result: ", result, "\n")

# for i, val in enumerate(result["messages"]):
#     print("Agent Response ", i, val.content, "\n")

app = FastAPI()

@app.get("/")
def returnHello():
    return {
        "response": "Hello World!"
    }

@app.post("/")
def recieveSignal(signal: dict):
    feature_threshold = signal["data"]["feature_threshold"]
    feature_name = signal["data"]["feature_name"]
    feature_value = signal["data"]["feature_value"]
    entity_type = signal["data"]["entity_type"]
    entity_id = signal["data"]["entity_id"]
    signal_name = signal["data"]["signal_name"]
    description = signal["data"]["description"]
    level = signal["data"]["level"]
    uuid = uuid4().hex[:8]
    case_file_name = f"Casebook_{feature_name}_{uuid}"
    Path(f"casebook/{case_file_name}.md").touch()

    agent_prompt = (
        f"The signal recieved is for {signal_name}"
        f"The feature for which investigation needs to carried out is {feature_name}, it has a feature threshold of {feature_threshold}, while the feature value recieved is {feature_value}"
        f"The investigation needs to carried out for entity type {entity_type} with an id of {entity_id}"
        f"The severity level of the signal recieved is {level}"
        f"The description of the event that has occured is {description}"
    )
    print(signal)
    result = agent.invoke({"messages":[{"role":"user", "content":agent_prompt}]})
    print("Final Response is ", result["messages"][-1].content)
    with open(f"casebook/{case_file_name}.md", "w") as f:
        f.write(result["messages"][-1].content)
    return {
        "result": result,
        "response": "signal recieved"
    }

# Signal Format for high_frequency_auth
# {
#   "eventId": "550e8400-e29b-41d4-a716-446655440000",
#   "eventTimestamp": "2024-05-20T14:30:00Z",
#   "eventVersion": "1.0.0",
#   "data": {
#     "feature_id": "F-99283",
#     "feature_threshold": 1000.0,
#     "feature_name": "high_frequency_auth_transactions",
#     "feature_value": 1250.5,
#     "entity_type": "operator",
#     "entity_id": "UPPRD_KHERI_NS917529",
#     "signal_id": "SIG-404",
#     "signal_name": "operator_auth",
#     "signal_version": "v2",
#     "description": "Operator has tried authentication with someone else's biometric",
#     "level": "high",
#     "created_at": "2024-05-20T14:29:55Z",
#     "comments": "Flagged by operator360 engine for manual review."
#   }
# }

# Signal Format for time anomalies
# {
#   "eventId": "550e8400-e29b-41d4-a716-446655440000",
#   "eventTimestamp": "2024-05-20T14:30:00Z",
#   "eventVersion": "1.0.0",
#   "data": {
#     "feature_id": "F-99283",
#     "feature_threshold": 1000.0,
#     "feature_name": "time_anomalies",
#     "feature_value": 1250.5,
#     "entity_type": "operator",
#     "entity_id": "UPPRD_KHERI_NS917529",
#     "signal_id": "SIG-404",
#     "signal_name": "operator_auth",
#     "signal_version": "v2",
#     "description": "Operator has tried authentication on off working hours",
#     "level": "high",
#     "created_at": "2024-05-20T14:29:55Z",
#     "comments": "Flagged by operator360 engine for manual review."
#   }
# }