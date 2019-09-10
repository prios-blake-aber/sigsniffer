
import logging
import objects
from result_sets import people, attributes, signals
import pandas as pd
from typing import List

logger = logging.getLogger(__name__)


def set_unicorn_path(unicorn_path):
    import sys
    sys.path.append(unicorn_path)


def all_signals_by_person(credentials: objects.SessionInfo,
                          signal_generator_ids: List[str]):

    logger.warning(f'Polling GQL for all people...')
    gql_people = people.PeopleQuery()
    person_response = gql_people.execute(credentials)
    logger.warning('...Polling people complete')

    available_people = person_response.df.personId.values
    if not available_people.any():
        logger.error('No people available!')
        return pd.DataFrame()

    logger.warning('Polling GQL for all attributes')
    gql_attributes = attributes.AttributeQuery()
    attr_response = gql_attributes.execute(credentials)
    logger.warning('...Polling attributes complete')

    results = list()
    logger.warning('Polling people now...')
    for person_id in available_people[:25]:
        logger.warning(f'Polling GQL for person_id: {person_id}')
        signal_response = signals.SignalsQuery(person_id, signal_generator_ids)
        results.append(signal_response.execute(credentials))
    signals_df = pd.concat([i.df for i in results])
    logger.warning('...Polling people complete')

    signals_df = pd.merge(signals_df, attr_response.df, how='left', on='attributeId')
    signals_df = pd.merge(signals_df, person_response.df, how='left', on='personId')

    return signals_df

