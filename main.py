import dash
import dash_auth
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly
from dash.dependencies import Input, Output, State
# from base_nadzor.pages import main_page, razr_str_layout, settings_layout, vvod_layout
from base_nadzor.pages import home, settings_layout, RSN_page
from base_nadzor.app import app

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Главная", href="/home"),
        dbc.DropdownMenuItem("Разрешения на строительство", href="/rns"),
        dbc.DropdownMenuItem("Разрешения на ввод", href="/rnv"),
        dbc.DropdownMenuItem("Настройки", href="/settings"),
    ],
    nav=True,
    in_navbar=True,
    label="Меню"
)

navbar = dbc.NavbarSimple(
    children=[
        dropdown,
        dbc.NavItem(dbc.NavLink("Главная", href="#")),
        dbc.NavItem(dbc.NavLink("О программе", href="#"))
    ],
    brand="УПРАВЛЕНИЕ АРХИТЕКТУРЫ И ГРАДОСТРОИТЕЛЬСТВА г.Махачкалы",
    brand_href="#",
    color="primary",
    dark=True,
    links_left=False
)

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'admin'
}


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/rns':
        return RSN_page.layout
    elif pathname == '/rns_new':
        return RSN_page.layout
    elif pathname == '/settings':
        return settings_layout.layout
    # elif pathname == '/rnv':
    #     return vvod_layout.layout


if __name__ == '__main__':
    app.run_server(debug=False)
