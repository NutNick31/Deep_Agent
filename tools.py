from langchain.tools import tool
from langgraph.types import interrupt

@tool(parse_docstring=True)
def ask_question(question: str):
    """Use this tool to ask questions whenever a clarification is needed between any tool calls or before starting any tool call or before starting the process itself"""
    answer = interrupt(question)
    return answer

@tool(parse_docstring=True)
def get_weather(location: str):
    """Get weather forecast of a location"""
    return f"The weather of {location} is sunny."

@tool(parse_docstring=True)
def get_person_info(name: str):
    """Get information about a person"""
    return f"The person {name} is a good person"

@tool(parse_docstring=True)
def get_trip_plan(location: str, weather: str):
    """Make the plan for a trip based the weather of a location"""
    # return f"The plan for the trip is {plan}"
    return f"The plan for the trip to {location} is great based on the weather which is {weather}"

TOOL_REGISTRY = [get_weather, get_person_info, get_trip_plan,ask_question]

# Dictionary for tool lookup by name if needed
TOOL_REGISTRY_BY_NAME = {"get_weather": get_weather, "get_person_info": get_person_info, "get_trip_plan": get_trip_plan, "ask_question":ask_question}

def get_tool_by_name(name: str):
    """This function returns tools from its name"""
    return TOOL_REGISTRY_BY_NAME[name]