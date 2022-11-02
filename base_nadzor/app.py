import dash
import dash_bootstrap_components as dbc

# bootstrap theme
external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets
                )
app.title = 'Надзор РСН и РНВ г.Махачкала'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

server = app.server

