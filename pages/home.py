import base64
import io
import time

import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, State

dash.register_page(__name__, path='/', order=0)

layout = html.Div([
    html.H1('Home page'),
    html.P('Please upload csv or xlsx file with data'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Not allow multiple files to be uploaded
        multiple=False
    ),
])


@callback(Output('store_df', 'data'),
          Output('store_df_columns', 'data'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          # prevent_initial_call=True,
          )
def update_store_df(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xlsx' in filename:
                # Assume that the user uploaded an Excel file
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                df = pd.DataFrame()
        except Exception as e:
            print(e)
            df = pd.DataFrame()
        return df.to_dict('records'), df.columns
    return dash.no_update
