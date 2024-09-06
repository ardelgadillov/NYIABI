import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, dash_table, ctx
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import plotly.express as px
import json

dash.register_page(__name__, icon='fas fa-chart-column me-4', order=2)

layout = html.Div([
    html.H1('Chart page'),
    html.P('Please select the chart type'),
    # chart options
    html.Div([
        dbc.Button(DashIconify(icon='carbon:chart-line', width=40, height=40, ),
                   color='primary', className='me-1', id='bt_line', n_clicks=0),
        dbc.Popover([dbc.PopoverHeader('Line Plot'), dbc.PopoverBody('Line Plot info')],
                    target='bt_line', trigger='hover', placement='bottom'),
        dbc.Button(DashIconify(icon='carbon:chart-scatter', width=40, height=40, ),
                   color='primary', className='me-1', id='bt_scatter', n_clicks=0),
        dbc.Popover([dbc.PopoverHeader('Scatter Plot'), dbc.PopoverBody('Scatter Plot info')],
                    target='bt_scatter', trigger='hover', placement='bottom'),
        dbc.Button(DashIconify(icon='carbon:chart-cluster-bar', width=40, height=40, ),
                   color='primary', className='me-1', id='bt_bar', n_clicks=0),
        dbc.Popover([dbc.PopoverHeader('Bar Plot'), dbc.PopoverBody('Bar Plot info')],
                    target='bt_bar', trigger='hover', placement='bottom'),
        dbc.Button(DashIconify(icon='carbon:chart-error-bar-alt', width=40, height=40, ),
                   color='primary', className='me-1', id='bt_box', n_clicks=0),
        dbc.Popover([dbc.PopoverHeader('Box Plot'), dbc.PopoverBody('Box Plot info')],
                    target='bt_box', trigger='hover', placement='bottom'),
    ]),
    html.Br(),
    # chart
    dbc.Row(
        [
            dbc.Col([
                html.H5('Parameters'),
                html.Div(id='chart_parameters')
            ], width=2),
            dbc.Col([
                dbc.Row(html.H5('Chart')),
                dcc.Graph(id='plotly_chart'),
                html.Br(),
                dbc.Row(html.H5('Python Code of the Plotly Chart')),
                dcc.Clipboard(target_id='plotly_code', title='Copy code'),
                dcc.Markdown(id='plotly_code'),
            ], width=10),
        ]
    ),
    # html.Br(),
    # html.Div(id='output_data_upload2'),
])


def plot_parameters(options, kind):
    if options is not None:
        parameters = [
            # First parameters in all charts
            dbc.Row([dbc.Label('x variable'),
                     dcc.Dropdown(options, id='dropdown_x', persistence=True)]),
            dbc.Row([dbc.Label('y variable'),
                     dcc.Dropdown(options, id='dropdown_y', persistence=True)]),
            dbc.Row([dbc.Label('color'),
                     dcc.Dropdown(options, id='dropdown_color', persistence=True)]),
            dbc.Row([dbc.Label('line group'),
                     dcc.Dropdown(options, id='dropdown_line_group', persistence=True)]
                    ) if kind == 'line' else html.Div(id='dropdown_line_group'),
            dbc.Row([dbc.Label('line dash'),
                     dcc.Dropdown(options, id='dropdown_line_dash', persistence=True)]
                    ) if kind == 'line' else html.Div(id='dropdown_line_dash'),
            dbc.Row([dbc.Label('symbol'),
                     dcc.Dropdown(options, id='dropdown_symbol', persistence=True)]
                    ) if kind == 'line' or kind == 'scatter' else html.Div(id='dropdown_symbol'),
            dbc.Row([dbc.Label('size'),
                     dcc.Dropdown(options, id='dropdown_size', persistence=True)]
                    ) if kind == 'scatter' else html.Div(id='dropdown_size'),
            dbc.Row([dbc.Label('text'),
                     dcc.Dropdown(options, id='dropdown_text', persistence=True)]
                    ) if kind == 'line' or kind == 'scatter' or kind == 'bar' else html.Div(id='dropdown_text'),
            dbc.Row([dbc.Label('hover_data'),
                     dcc.Dropdown(options, id='dropdown_hover_data', persistence=True)]),
            dbc.Row([dbc.Label('facet_row'),
                     dcc.Dropdown(options, id='dropdown_facet_row', persistence=True)]),
            dbc.Row([dbc.Label('facet_col'),
                     dcc.Dropdown(options, id='dropdown_facet_col', persistence=True)]),
            dbc.Row([dbc.Label('animation_frame'),
                     dcc.Dropdown(options, id='dropdown_animation_frame', persistence=True)]),
            dbc.Row([dbc.Label('animation_group'),
                     dcc.Dropdown(options, id='dropdown_animation_group', persistence=True)]),
        ]
        return html.Div(parameters)


def line_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
              animation_frame, animation_group, df, chart):
    fig = px.line(df, x=x, y=y, color=color, line_group=line_group, line_dash=line_dash, symbol=symbol,
                  hover_data=hover_data, text=text, facet_row=facet_row, facet_col=facet_col,
                  animation_frame=animation_frame, animation_group=animation_group)
    x_str = f'x="{x}", ' if x is not None else ""
    y_str = f'y="{y}", ' if y is not None else ""
    color_str = f'color="{color}", ' if color is not None else ""
    line_group_str = f'line_group="{line_group}", ' if line_group is not None else ""
    line_dash_str = f'line_dash="{line_dash}", ' if line_dash is not None else ""
    symbol_str = f'symbol="{symbol}", ' if symbol is not None else ""
    hover_data_str = f'hover_data="{hover_data}", ' if hover_data is not None else ""
    text_str = f'text="{text}", ' if text is not None else ""
    facet_row_str = f'facet_row="{facet_row}", ' if facet_row is not None else ""
    facet_col_str = f'facet_col="{facet_col}", ' if facet_col is not None else ""
    animation_frame_str = f'animation_frame="{animation_frame}", ' if animation_frame is not None else ""
    animation_group_str = f'animation_group="{animation_group}", ' if animation_group is not None else ""

    code = f'''
                    ```python

                    import plotly.express as px
                    df = pd.Dataframe()  # df is a pandas DataFrame
                    fig = px.line(df, {x_str}{y_str}{color_str}{line_group_str}{line_dash_str}{symbol_str}{hover_data_str}{text_str}{facet_row_str}{facet_col_str}{animation_frame_str}{animation_group_str})
                    fig.show()
                    ``` '''
    return fig, code


def scatter_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
                 animation_frame, animation_group, df, chart):
    fig = px.scatter(df, x=x, y=y, color=color, symbol=symbol, size=size, text=text, hover_data=hover_data,
                     facet_row=facet_row, facet_col=facet_col, animation_frame=animation_frame,
                     animation_group=animation_group)
    x_str = f'x="{x}", ' if x is not None else ""
    y_str = f'y="{y}", ' if y is not None else ""
    color_str = f'color="{color}", ' if color is not None else ""
    symbol_str = f'symbol="{symbol}", ' if symbol is not None else ""
    size_str = f'size="{size}", ' if size is not None else ""
    text_str = f'text="{text}", ' if text is not None else ""
    hover_data_str = f'hover_data="{hover_data}", ' if hover_data is not None else ""
    facet_row_str = f'facet_row="{facet_row}", ' if facet_row is not None else ""
    facet_col_str = f'facet_col="{facet_col}", ' if facet_col is not None else ""
    animation_frame_str = f'animation_frame="{animation_frame}", ' if animation_frame is not None else ""
    animation_group_str = f'animation_group="{animation_group}", ' if animation_group is not None else ""

    code = f'''
                    ```python

                    import plotly.express as px
                    df = pd.Dataframe()  # df is a pandas DataFrame
                    fig = px.scatter(df, {x_str}{y_str}{color_str}{symbol_str}{size_str}{text_str}{hover_data_str}{facet_row_str}{facet_col_str}{animation_frame_str}{animation_group_str})
                    fig.show()
                    ``` '''
    return fig, code


def bar_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
             animation_frame, animation_group, df, chart):
    fig = px.bar(df, x=x, y=y, color=color, text=text, hover_data=hover_data,
                 facet_row=facet_row, facet_col=facet_col, animation_frame=animation_frame,
                 animation_group=animation_group)
    x_str = f'x="{x}", ' if x is not None else ""
    y_str = f'y="{y}", ' if y is not None else ""
    color_str = f'color="{color}", ' if color is not None else ""
    text_str = f'text="{text}", ' if text is not None else ""
    hover_data_str = f'hover_data="{hover_data}", ' if hover_data is not None else ""
    facet_row_str = f'facet_row="{facet_row}", ' if facet_row is not None else ""
    facet_col_str = f'facet_col="{facet_col}", ' if facet_col is not None else ""
    animation_frame_str = f'animation_frame="{animation_frame}", ' if animation_frame is not None else ""
    animation_group_str = f'animation_group="{animation_group}", ' if animation_group is not None else ""

    code = f'''
                    ```python

                    import plotly.express as px
                    df = pd.Dataframe()  # df is a pandas DataFrame
                    fig = px.bar(df, {x_str}{y_str}{color_str}{text_str}{hover_data_str}{facet_row_str}{facet_col_str}{animation_frame_str}{animation_group_str})
                    fig.show()
                    ``` '''
    return fig, code


def box_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
             animation_frame, animation_group, df, chart):
    fig = px.box(df, x=x, y=y, color=color, hover_data=hover_data,
                 facet_row=facet_row, facet_col=facet_col, animation_frame=animation_frame,
                 animation_group=animation_group)
    x_str = f'x="{x}", ' if x is not None else ""
    y_str = f'y="{y}", ' if y is not None else ""
    color_str = f'color="{color}", ' if color is not None else ""
    hover_data_str = f'hover_data="{hover_data}", ' if hover_data is not None else ""
    facet_row_str = f'facet_row="{facet_row}", ' if facet_row is not None else ""
    facet_col_str = f'facet_col="{facet_col}", ' if facet_col is not None else ""
    animation_frame_str = f'animation_frame="{animation_frame}", ' if animation_frame is not None else ""
    animation_group_str = f'animation_group="{animation_group}", ' if animation_group is not None else ""

    code = f'''
                    ```python

                    import plotly.express as px
                    df = pd.Dataframe()  # df is a pandas DataFrame
                    fig = px.box(df, {x_str}{y_str}{color_str}{hover_data_str}{facet_row_str}{facet_col_str}{animation_frame_str}{animation_group_str})
                    fig.show()
                    ``` '''
    return fig, code


@callback(Output('plotly_chart', 'figure'),
          Output('plotly_code', 'children'),
          Input('dropdown_x', 'value'),
          Input('dropdown_y', 'value'),
          Input('dropdown_color', 'value'),
          Input('dropdown_line_group', 'value'),
          Input('dropdown_line_dash', 'value'),
          Input('dropdown_symbol', 'value'),
          Input('dropdown_size', 'value'),
          Input('dropdown_text', 'value'),
          Input('dropdown_hover_data', 'value'),
          Input('dropdown_facet_row', 'value'),
          Input('dropdown_facet_col', 'value'),
          Input('dropdown_animation_frame', 'value'),
          Input('dropdown_animation_group', 'value'),
          State('store_df', 'data'),
          State('store_chart', 'data')
          )
def plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
         animation_frame, animation_group, df, chart):
    try:
        if chart == 'line':
            return line_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
                             animation_frame, animation_group, df, chart)
        elif chart == 'scatter':
            return scatter_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row,
                                facet_col, animation_frame, animation_group, df, chart)
        elif chart == 'bar':
            return bar_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
                            animation_frame, animation_group, df, chart)
        elif chart == 'box':
            return box_plot(x, y, color, line_group, line_dash, symbol, size, text, hover_data, facet_row, facet_col,
                            animation_frame, animation_group, df, chart)
    except:
        print('some error')
        return dash.no_update, dash.no_update


@callback(Output('chart_parameters', 'children'),
          Output('store_chart', 'data'),
          Input('bt_line', 'n_clicks'),
          Input('bt_scatter', 'n_clicks'),
          Input('bt_bar', 'n_clicks'),
          Input('bt_box', 'n_clicks'),
          State('store_df_columns', 'data'),
          State('store_chart', 'data')
          )
def on_plot_click(bt_line_n_clicks, bt_scatter_n_clicks, bt_bar_n_clicks, bt_box_n_clicks, df_columns, chart):
    if 'bt_line' == ctx.triggered_id:
        if bt_line_n_clicks > 0:
            store = 'line'
        else:
            store = chart
        children = plot_parameters(df_columns, store)
    elif 'bt_scatter' == ctx.triggered_id:
        store = 'scatter'
        children = plot_parameters(df_columns, store)
    elif 'bt_bar' == ctx.triggered_id:
        store = 'bar'
        children = plot_parameters(df_columns, store)
    elif 'bt_box' == ctx.triggered_id:
        store = 'box'
        children = plot_parameters(df_columns, store)
    else:
        children = dash.no_update
        store = dash.no_update
    return children, store

# @callback(Output('output_data_upload2', 'children'),
#           Input('store_df', 'data'))
# def update_output_data_upload(data):
#     return html.Div([
#         # html.H5(filename),
#         # html.H6(datetime.datetime.fromtimestamp(date)),
#         dash_table.DataTable(
#             data,
#             # df.to_dict('records'),
#             # [{'name': i, 'id': i} for i in df.columns],
#
#             style_header={
#                 'backgroundColor': 'rgb(30, 30, 30)',
#                 'color': 'white',
#                 'fontWeight': 'bold'
#             },
#             style_data={
#                 'backgroundColor': 'rgb(50, 50, 50)',
#                 'color': 'white'
#             },
#             style_data_conditional=[
#                 {
#                     'if': {'row_index': 'even'},
#                     'backgroundColor': 'rgb(220, 220, 220)',
#                     'color': 'rgb(50, 50, 50)'
#                 }
#             ],
#         ),
#     ])
