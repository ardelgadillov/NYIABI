import dash_bootstrap_components as dbc
import pandas as pd
import dash
from dash import html, dcc


def df_from_dict(dict_data):
    df = pd.DataFrame.from_dict(dict_data, orient='tight')
    return df


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


def dbc_widget(widget, label, **kwargs):
    return html.Div([
        dbc.Label(label, size='sm'),
        widget(size='sm', **kwargs),
    ])


def dbc_modal(title, body, id):
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title)),
        dbc.ModalBody(body)
    ], id=id, is_open=False)


# @cache.cached(timeout=3600 * 24)
def read_bess_db():
    xls = pd.ExcelFile(r'data\bess_db.xlsx')
    bess_df = pd.read_excel(xls, 'Vendors', index_col='ID')
    initial_data = {'index': bess_df.index[0],
                    'country': bess_df['Country'].iloc[0],
                    'vendor': bess_df['Vendor'].iloc[0],
                    'date': bess_df['Date'].iloc[0]}
    bess_df = bess_df.to_dict('tight')
    ltsa_df = pd.read_excel(xls, 'LTSA', index_col='ID').to_dict('tight')
    rte_df = pd.read_excel(xls, 'RTE', index_col='ID').to_dict('tight')
    soh_df = pd.read_excel(xls, 'SOH', index_col='ID').to_dict('tight')
    xls.close()
    print('read bess file')
    return bess_df, ltsa_df, rte_df, soh_df, initial_data


def read_bnef():
    xls = pd.ExcelFile(r'data\bnef_raw_data.xlsx')
    bnef_df = pd.read_excel(xls, 'Raw', index_col=[0, 1, 2, 3, 4]).round(2).to_dict('tight')
    bnef_definition = pd.read_excel(xls, 'Definition', index_col=0).to_dict('tight')
    xls.close()
    print('read bnef file')
    return bnef_df, bnef_definition


def sidebar(title):
    return html.Div(
        [
            html.Div(
                html.Img(src='/assets/logo.png', style={'height': '80%', 'width': '80%'}),
                className='sidebar-header'
            ),
            html.Br(),
            html.Div([
                html.H2(title),
            ],
                className='sidebar-header',
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink([
                        html.Div([
                            html.I(className=page['icon']),
                            html.Span(page['name'])
                        ])
                    ],
                        href=page['path'],
                        active='exact', )
                    for page in dash.page_registry.values()
                ],
                vertical=True, pills=True,
            ),
        ],
        className='sidebar'
    )


def content():
    return html.Div(dash.page_container, id='page-content', className='content')


class ButtonDisableDuringCallbackDiv(html.Div):
    """Helper div to create a button that is associated with a long running
    computation. Linking a callback to the 'button_id' inside this div will
    cause the button to be disabled for the duration of the computation if the
    callback uses the trigger div as output:

        button_div = ButtonDisableDuringCallbackDiv("button", "Submit")

        @app.callback(
            Output(button_div.trigger_div.id, "children"),
            [Input(button_div.id)]
        )
        def handle_button_click(n_clicks):
            # do long compute
            import time
            time.sleep(10)
            # something must be returned to the trigger div
            return 1

    Args:
        name (str): Name used as the prefix for ids. Should be unique.
        display_label (str): String to display on the button.
    """

    def __init__(self, name, display_label):
        self.name = name
        self.trigger_div = html.Div(id=f"{name}_trigger_id", hidden=True)
        self.button = dbc.Button(children=display_label, id=f"{name}_button_id", color="primary")
        self.loading = dcc.Loading([self.button, self.trigger_div], type="circle")
        super().__init__(self.loading, id=f"{name}_div_id")
