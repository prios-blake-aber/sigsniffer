
import pandas as pd
from dataclasses import dataclass

import objects


@dataclass
class AttributeQuery(objects.GraphQlResultSet):

    def query(self):
        return """
            query attributes {
              v2{
                attributes(labels: AGGREGATED){
                  name
                  attributeId
                }
              }
            }
        """

    def transform(self, response):
        x = response.get("data", {}).get("v2", {}).get("attributes", {})
        df = pd.DataFrame.from_records(x)
        df.columns = ['attributeName', 'attributeId']
        return df

