import dash
from dash import html, callback, Input, Output, State, dash_table

dash.register_page(__name__, icon='fas fa-arrow-trend-up me-4', order=1)

layout = html.Div([
    html.H1('Dataset page'),
    html.P('This is the table with the data'),
    # data table
    html.Div(id='output_data_upload'),
])


@callback(Output('output_data_upload', 'children'),
          Input('store_df', 'data'),
          )
def update_output_data_upload(data):
    return html.Div([
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        dash_table.DataTable(
            data,
            export_format="csv",
            # df.to_dict('records'),
            # [{'name': i, 'id': i} for i in df.columns],

            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                    'color': 'rgb(50, 50, 50)'
                }
            ],
        ),
    ])
