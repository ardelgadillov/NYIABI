import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas
import plotly.express as px
from utils import sidebar, content

external_stylesheets = [dbc.themes.FLATLY, dbc.icons.FONT_AWESOME]
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)


sidebar_app = sidebar('BI tool')
content_app = content()

app.layout = html.Div(
    [
        dcc.Store(id='store_df', data=None),
        dcc.Store(id='store_df_columns', data=None),
        dcc.Store(id='store_chart', data=None, storage_type='local'),
        dcc.Location(id='url'),
        sidebar_app,
        content_app,
     ]
)

if __name__ == '__main__':
    app.run(debug=False)
