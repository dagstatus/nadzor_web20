import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


class EditRSNForm:
    def __init__(self):
        self.result = None
