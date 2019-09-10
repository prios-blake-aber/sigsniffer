
import pandas as pd
from dataclasses import dataclass

import objects


@dataclass
class PeopleQuery(objects.GraphQlResultSet):

    def query(self):
        return """
            query people {
              v2 {
                people(limit: 10000){
                  edges{
                    node{
                      personId
                      name
                    }
                  }
                }
              }
            }
        """

    def transform(self, response, **kwargs):
        x = response.get("data", {}).get("v2", {}).get("people", {}).get("edges", {})
        x = [i.get("node") for i in x]
        df = pd.DataFrame.from_records(x)
        df.columns = ['personName', 'personId']
        return df
