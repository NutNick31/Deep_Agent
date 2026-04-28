import pandas as pd
import sqlite3

def dbWrapper(type: str, table_csv_name: str, entity_feature: str, entity_value: str):
    if type=="csv":
        print("CSV Wrapper")
        df = pd.read_csv(table_csv_name)
        collected_rows = df[df[entity_feature]==entity_value]
        return collected_rows
    else:
        # Code for calling SQL table, after getting appropriate api's and tables
        print("SQL Wrapper")