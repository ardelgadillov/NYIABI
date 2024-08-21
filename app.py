import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas
import plotly.express as px

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div(
    [
        html.H2('NyiaBI', className='display-4'),
        html.Hr(),
        html.P('A simple BI tool to plot data with Plotly', className='lead'),
        dbc.Nav(
            [
                dbc.NavLink([html.Div(page['name'], className='ms-2'), ],
                            href=page['path'], active='exact',)
                for page in dash.page_registry.values()
            ],
            vertical=True, pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(dash.page_container, id='page-content', style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Store(id='store_df', data=None),
        dcc.Store(id='store_df_columns', data=None),
        dcc.Store(id='store_chart', data=None, storage_type='local'),
        dcc.Location(id='url'),
        sidebar,
        content,
     ]
)

if __name__ == '__main__':
    # df = px.data.gapminder()
    # df.to_csv(r'C:\Users\AndresDelgadillo\Downloads\gap.csv')
    app.run(debug=True)
