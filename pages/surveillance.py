
import pandas as pd

from app import app, dt, dcc, html, Input, Output

import config, functions

df = functions.all_signals_by_person(
    config.STAGING, signal_generator_ids=['fa2dce36-c775-42bd-85f6-6bdf20bd7c1d']
)
# add an id column and set it as the index
# in this case the unique ID is just the country name, so we could have just
# renamed 'country' to 'id' (but given it the display name 'country'), but
# here it's duplicated just to show the more general pattern.
df['id'] = df['signalGeneratorId']
df.set_index('id', inplace=True, drop=False)
df['signalValue'] = df['signalValue'].apply(lambda x: str(x))

layout = html.Div([
    html.Div([
        dcc.Input(
            id='endpoint_id',
            placeholder='Endpoint...',
            type='text',
            value=''),
        dcc.Input(
            id='group_token_id',
            placeholder='Group-Token...',
            type='text',
            value=''),
        dcc.Input(
            id='session_token_id',
            placeholder='Session-Token...',
            type='text',
            value=''),
    ]),
    dt.DataTable(
        id='datatable-row-ids',
        style_data={'whiteSpace': 'normal'},
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
    ),
    # html.Div(id='datatable-row-ids-container')
])


# @app.callback(
#     Output('datatable-row-ids-container', 'children'),
#     [Input('datatable-row-ids', 'derived_virtual_row_ids'),
#      Input('datatable-row-ids', 'selected_row_ids'),
#      Input('datatable-row-ids', 'active_cell')])
# def update_graphs(row_ids, selected_row_ids, active_cell):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncracy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     selected_id_set = set(selected_row_ids or [])
#
#     if row_ids is None:
#         dff = df
#         # pandas Series works enough like a list for this to be OK
#         row_ids = df['id']
#     else:
#         dff = df.loc[row_ids]
#
#     active_row_id = active_cell['row_id'] if active_cell else None
#
#     colors = ['#FF69B4' if id == active_row_id
#               else '#7FDBFF' if id in selected_id_set
#               else '#0074D9'
#               for id in row_ids]
#
#     return [
#         dcc.Graph(
#             id=column + '--row-ids',
#             figure={
#                 'data': [
#                     {
#                         'x': dff['signalGeneratorId'],
#                         'y': dff[column],
#                         'type': 'bar',
#                         'marker': {'color': colors},
#                     }
#                 ],
#                 'layout': {
#                     'xaxis': {'automargin': True},
#                     'yaxis': {
#                         'automargin': True,
#                         'title': {'text': column}
#                     },
#                     'height': 250,
#                     'margin': {'t': 10, 'l': 10, 'r': 10},
#                 },
#             },
#         )
#         # check if column exists - user may have deleted it
#         # If `column.deletable=False`, then you don't
#         # need to do this check.
#         for column in dff
#     ]
