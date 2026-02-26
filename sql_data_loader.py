"""
sql_data_loader.py

Purpose:
---------
This module provides the SQLDataLoader class responsible for handling database connectivity and data extraction from SQL Server
for the London Airbnb Quarterly Analysis project.

It abstracts the database interaction layer from the main pipeline, ensuring a clean separation between data extraction and data
transformation logic.

Key Responsibilities:
----------------------
1. Establish a connection to SQL Server using SQLAlchemy.
2. Execute SQL queries and load results into a Pandas DataFrame.
3. Provide a reusable and modular interface for database operations.

Design Philosophy:
-------------------
- Separation of concerns (database access isolated from cleaning logic).
- Reusable connection engine.
- Scalable for future expansion (additional queries, inserts, updates).
- Compatible with production-style ETL workflows.

This module enables seamless integration between SQL Server and Python-based data processing using Pandas.

Author: Sonali Patel
Project: London Airbnb Quarterly Performance Analysis
"""
import pandas as pd
from sqlalchemy import create_engine

class SQLDataLoader:

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def fetch_data(self, query: str):

        return pd.read_sql(query, self.engine)
