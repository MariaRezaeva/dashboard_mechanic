import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from pages.plant import mechanic
from pages import home
from pages.analytic import retrospective
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


sidebar = html.Div(
    [
        html.Div('ZCMC', className='logo'),
        html.Div(style={'height':'15px'}),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="uil uil-estate", style={"margin-right":"10px"}), "Главная"],
                            href="/pages/home", id="page-1-link", className='navlink_style'),
                dbc.NavLink(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem("Прогноз", href="#"),
                                  dbc.DropdownMenuItem("Ретроспектива", href='/pages/analytic/retrospective')],
                        label=[html.I(className="uil-graph-bar", style={"margin-right": "10px"}),
                               "Аналитика"],
                        nav=True,
                        toggleClassName='navlink_style',

                    ), href="#", id="page-2-link", className='navlink_style'),
                dbc.NavLink(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem("Служба главного механика", href="/pages/plant/mechanic"),
                                  dbc.DropdownMenuItem("Служба главного энергетика", href='#'),
                                  dbc.DropdownMenuItem("Служба главного автоматика", href='#'),
                                  ],

                        label=[html.I(className="fa fa-industry", style={"margin-right": "10px"}),
                               "Фабрика"],
                        nav=True,
                        toggleClassName='navlink_style',
                    ), href="#", id="page-3-link", className='navlink_style'),
                dbc.NavLink(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem("Движение техники", href="#"),
                                  dbc.DropdownMenuItem("Выработка и простои", href='#'),
                                  ],

                        label=[html.I(className="uil uil-shovel", style={"margin-right": "10px"}),
                               "Карьер"],
                        nav=True,
                        toggleClassName='navlink_style',
                    ), href="#", id="page-4-link", className='navlink_style'),

                dbc.NavLink(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem("Фабрика", href="#"),
                                  dbc.DropdownMenuItem("Карьер", href='#'),
                                  ],

                        label=[html.I(className="uil uil-clipboard-alt", style={"margin-right": "10px"}),
                               "Заявки на ремонт"],
                        nav=True,
                        toggleClassName='navlink_style',
                    ), href="#", id="page-5-link", className='navlink_style'),

                dbc.NavLink(
                    dbc.DropdownMenu(
                            children = [dbc.DropdownMenuItem("Конвееры", href='#'),
                                        dbc.DropdownMenuItem("Мельницы", href='#'),],
                            label=[html.I(className="fa fa-camera", style={"margin-right": "10px"}),
                                   "Видеокамеры"],
                            nav=True,
                            toggleClassName = 'navlink_style',

                        ), href="#", id="page-6-link", className='navlink_style'),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    className='sidebar_style',
)

content = html.Div(
    id="page-content",
    className='content_style')

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        html.Div([
            sidebar,
            html.Div([
                html.Div([html.Button([html.I(className="bx bx-menu", style={"font-size":"55px"})], className="button_hamburger", id="btn_sidebar"),
                          ], className='header_show', id = 'header_'),

                html.Div(content, style={'background':'green'}),
            ]),
        ]),

    ],
)


@app.callback(
    [
        Output("sidebar", "className"),
        Output("page-content", "className"),
        Output("side_click", "data"),
        Output("header_", "className"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = 'sidebar_hidden'
            content_style = 'content_style_1'
            cur_nclick = "HIDDEN"
            header_output  = 'header_hidden'
        else:
            sidebar_style = 'sidebar_style'
            content_style = 'content_style'
            cur_nclick = "SHOW"
            header_output = 'header_show'
    else:
        sidebar_style = 'sidebar_style'
        content_style = 'content_style'
        cur_nclick = 'SHOW'
        header_output = 'header_show'

    return sidebar_style, content_style, cur_nclick, header_output

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/pages/home":
        return home.main_layout
    elif pathname == '/pages/analytic/retrospective':
        return retrospective.retrospective_layout
    elif pathname == "/pages/plant/mechanic":
        return mechanic.mechanic_layout

        # If the user tries to reach a differe;nt page, return a 404 message

if __name__ == "__main__":
    #app.run_server(debug=True, port=8086)
    app.run_server(debug=False, port=8086, host='0.0.0.0')