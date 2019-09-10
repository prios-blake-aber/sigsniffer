
from dataclasses import dataclass
import requests
import pandas as pd


@dataclass
class SessionInfo:
    endpoint: str
    group_token: str
    session_token: str


@dataclass
class GraphQlResponse:
    response: str
    df: pd.DataFrame


@dataclass
class GraphQlResultSet:

    def query(self) -> str:
        raise NotImplementedError

    def transform(self, response, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def execute(self, credentials: SessionInfo, **kwargs):
        response = requests.post(
            url=credentials.endpoint,
            json={'query': self.query()},
            headers={'Group-Token': credentials.group_token,
                     'Session-Token': credentials.session_token}).json()
        df = self.transform(response, **kwargs)
        return GraphQlResponse(response, df)
