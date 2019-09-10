
import json
import pandas as pd
from typing import List
from dataclasses import dataclass, field

import objects, config
from result_sets import people, attributes


def extract_signal(one_signal):
    reformat = dict()
    reformat['signalGeneratorId'] = one_signal.get("signalGeneratorId")
    reformat['createdAt'] = one_signal.get("createdAt")

    reformat['personId'] = None
    reformat['attributeId'] = None
    signal_subjects = one_signal.get("subjects")
    if signal_subjects is not None and len(signal_subjects) > 0:
        for x in signal_subjects:
            if x['type'] == 'person':
                reformat['personId'] = x['entityId']
            if x['type'] == 'attribute':
                reformat['attributeId'] = x['entityId']

    signal_values = one_signal.get("signalValue", {}).get("asJson", {})
    if signal_values != 'null':
        reformat['signalValue'] = json.loads(signal_values)
    else:
        reformat['signalValue'] = None
    return reformat


@dataclass
class SignalsQuery(objects.GraphQlResultSet):
    person_id: str
    signal_generator_ids: List[str]

    def query(self):
        return """
            query signal_values {{
            v2 {{
                signals {{
                    queryIndex(
                        signalGeneratorIds: ["{signal_generator_ids}"],
                        entityType: person,
                        subjectId: "{person_id}"
                        ){{
                            signalGeneratorId
                            createdAt
                            subjects {{
                              type
                              entityId
                            }}
                            signalValue {{
                              asJson
                            }}
                          }}
                        }}
                  }}
                }}
        """.format(person_id=self.person_id,
                   signal_generator_ids="\",\"".join(self.signal_generator_ids))

    def transform(self, response):
        signals = response.get('data', {}).get('v2', {}).get("signals", {}).get(
            "queryIndex")

        if signals is None or len(signals) == 0:
            return pd.DataFrame()

        signal_df = pd.DataFrame.from_records([extract_signal(x) for x in signals])
        person_df = people.PeopleQuery.execute(config.STAGING)
        attr_df = attributes.AttributeQuery.execute(config.STAGING)

        signal_df = pd.merge(attr_df, signal_df, how='left', on='attributeId')
        signal_df = pd.merge(person_df, signal_df, how='left', on='personId')

        return signal_df
