from app import create_app, db, cli
from app.models import User, Post, Notification, Message, Task
from flask_login import login_required

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

app = create_app()
cli.register(app)

# dashapp = dash.Dash(__name__, server=app, url_base_pathname='/renderDashApp/')


# def protect_dashviews(dashapp):
#     for view_func in dashapp.server.view_functions:
#         if view_func.startswith(dashapp.url_base_pathname):
#             dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


# protect_dashviews(dashapp)

# dashapp.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 
    'Message':Message, 'Notification':Notification,
    'Task':Task}
