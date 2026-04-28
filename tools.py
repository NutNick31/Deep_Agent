import pandas as pd
from langchain.tools import tool
from langgraph.types import interrupt

@tool
def ask_question(question: str):
    """Use this tool to ask questions whenever a clarification is needed between any tool calls or before starting any tool call or before starting the process itself"""
    answer = interrupt(question)
    return answer

@tool
def scan_db_for_operator_auth_for_high_frequency_transaction(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_high_frequency_transaction tool was called")
    return operator_auth_tranasctions

@tool
def scan_db_for_operator_auth_for_geo_inconsistency(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_for_geo_inconsistency tool was called")
    return operator_auth_tranasctions

@tool
def scan_db_for_operator_auth_for_time_anomalies(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_for_time_anomalies tool was called")
    return operator_auth_tranasctions

@tool
def scan_db_for_operator_auth_for_device_sharing(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_for_device_sharing tool was called")
    return operator_auth_tranasctions

@tool
def scan_db_for_operator_auth_for_failure_success_bursts(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_for_failure_success_bursts tool was called")
    return operator_auth_tranasctions

@tool
def scan_db_for_operator_auth_for_biometric_abuse(operator_id: str):
    """Extract all the rows from the csv file correspoding to an operator when the case is for high frequency auth transactions"""
    df = pd.read_csv("db/Operator_Auth.csv")
    operator_auth_tranasctions = df[df['Opt ID']==operator_id]
    print("scan_db_for_operator_auth_for_biometric_abuse tool was called")
    return operator_auth_tranasctions

TOOL_REGISTRY_BY_NAME = {
    "ask_question":ask_question,
    "scan_db_for_operator_auth_for_high_frequency_transaction": scan_db_for_operator_auth_for_high_frequency_transaction,
    "scan_db_for_operator_auth_for_geo_inconsistency": scan_db_for_operator_auth_for_geo_inconsistency,
    "scan_db_for_operator_auth_for_time_anomalies": scan_db_for_operator_auth_for_time_anomalies,
    "scan_db_for_operator_auth_for_device_sharing": scan_db_for_operator_auth_for_device_sharing,
    "scan_db_for_operator_auth_for_failure_success_bursts": scan_db_for_operator_auth_for_failure_success_bursts,
    "scan_db_for_operator_auth_for_biometric_abuse": scan_db_for_operator_auth_for_biometric_abuse,
}

def get_tool_by_name(name: str):
    """This function returns tools from its name"""
    return TOOL_REGISTRY_BY_NAME[name]