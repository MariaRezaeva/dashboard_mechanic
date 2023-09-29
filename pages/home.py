import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

main_layout = html.Div([
    html.H1('Page main'),
    html.P('Content for Page main')
], className="mec")