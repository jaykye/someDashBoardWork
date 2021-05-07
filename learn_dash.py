import plotly.express as px
from jupyter_dash import JupyterDash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Build App

app = JupyterDash(__name__)
app.layout = html.Div([

    # Left column Div
    html.Div([
        html.Div([
            html.H1("Figure 1"),
            dash_table.DataTable(
                id='table_1',
                page_action='native',
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=10,
                style_table={'box-sizing': 'inherit', 'overflowX': 'auto', 'overflowY': 'auto'}),
            html.Label([
                "Select a Platform",
                dcc.Dropdown(
                    id='platform', clearable=False,
                    value='NES', options=[
                        {'label': p, 'value': p} for p in df['Platform'].unique()
                    ])
            ])
        ], style=figure_style),

        html.Div([
            html.H1("Figure 3"),
            dcc.Graph(id='figure_3'),
            html.Label([
                "colorscale",
                dcc.Dropdown(
                    id='colorscale-dropdown_3', clearable=False,
                    value='plasma', options=[
                        {'label': c, 'value': c}
                        for c in px.colors.named_colorscales()
                    ])
            ])
        ], style=figure_style)
    ],
        style=column_styles, className='left column'),

    # Right column Div
    html.Div([
        html.Div([
            html.H1("Figure 2"),
            dcc.Graph(id='figure_2'),
            html.Label([
                "Select a Publisher",
                dcc.Dropdown(
                    id='publisher', clearable=False,
                    value='Nintendo', options=[
                        {'label': c, 'value': c}
                        for c in big_pubs  # Dropdown에 항목이 너무 많으면 안됨. -- 아예 안만들어줌.
                    ])
            ])
        ], style=figure_style),
        html.Div([
            html.H1("Figure 4"),
            dcc.Graph(id='figure_4',
                      figure=px.pie(recent_publisher_mkt_share,
                                    values='Global_Sales',
                                    names='Publisher',
                                    title='Publisher Market share Since 2020',
                                    hole=0.3)),
        ], style=figure_style)
    ], style=column_styles, className='right column')

], style={'box-sizing': 'border-box', 'background-color': '#ECECEC', 'height': '100%', 'display': 'flex'},
    className='MainDiv')
# 'height': '100%', 'display':'flex' 이게 중요하네.


############ Figure 1 ############
target = 1


@app.callback(
    Output(f'table_{target}', 'data'),  # id, what to change
    [Input(f"platform", "value")]  # id, what to read
)
def update_table_1(platform):
    data = df.loc[df['Platform'] == platform]
    columns = [{"name": i, "id": i} for i in data.columns]
    return data.to_dict('records')


############ Figure 2 ############
@app.callback(
    Output(f'figure_2', 'figure'),  # id, what to change
    [Input("publisher", "value")]  # id, what to read
)
def update_figure_2(publisher):
    pulisher_sales_df = df.groupby(['Publisher', 'Year'])[['Global_Sales']].sum().reset_index('Year')
    return px.bar(
        pulisher_sales_df.loc[publisher], x="Year", y="Global_Sales",
        #         color="size",
        #         color_continuous_scale=colorscale,
        #         render_mode="webgl",
        title="Publisher Sales"
    )


############ Figure 3 ############
# target = 3
# @app.callback(
#     Output(f'figure_{target}', 'figure'),  # id, what to change
#     [Input(f"colorscale-dropdown_{target}", "value")]  # id, what to read
# )
# def update_figure_3(colorscale):
#     return px.scatter(
#         df, x="total_bill", y="tip", color="size",
#         color_continuous_scale=colorscale,
#         render_mode="webgl", title="Tips"
#     )

############ Figure 4 ############
# target = 4
# @app.callback(
#     Output(f'figure_{target}', 'figure'),  # id, what to change
#     [Input(f"colorscale-dropdown_{target}", "value")]  # id, what to read
# )
# def update_figure_3(colorscale):
#     return px.scatter(
#         df, x="total_bill", y="tip", color="size",
#         color_continuous_scale=colorscale,
#         render_mode="webgl", title="Tips"
#     )

# Run app and display result inline in the notebook
app.run_server(mode='external')




# table

dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="multi",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    )