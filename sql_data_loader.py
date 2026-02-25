import pandas as pd
from sqlalchemy import create_engine


class SQLDataLoader:

    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def fetch_data(self, query: str):
        return pd.read_sql(query, self.engine)