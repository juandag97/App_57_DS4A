import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash import Dash
from server_flask import server

# Connection to the database
from server_flask import con

##########FIGURE MAP
import plotly.express as px
import plotly.graph_objects as go

Coordinate_List=[

    # (18.49,-67.14),
    # (18.45,-66.18),
    (10.41,-75.58),
    (4.29,-74.82),
    (9.73,-75.06),
    (10.97,-73.54),
    (9.73,-73.86),
    (11.33,-72.74),
    (8.53,-76.70),
    (8.05,-75.18),
    (8.77,-75.86),
    (10.69,-74.86),
    (10.49,-74.34),
    (10.41,-75.58),
    (8.93,-75.46),
    (8.21,-76.38),
    (9.17,-75.30),
    (7.85,-76.82),
    (6.73,-76.70),
    (10.77,-73.98),
    (8.37,-74.90),
    (7.33,-75.78),
    (9.05,-74.10),
    (4.29,-74.82),
    (10.45,-73.18),
    (10.21,-74.90)
]

# # Testing Query
# query = 'SELECT * FROM consumption'
# consumption = pd.read_sql(query,con)
# print (consumption)

map_app1 = Dash(__name__, suppress_callback_exceptions=True, server = server, url_base_pathname='/dashmap/')

longitude=[tup[0] for tup in Coordinate_List]
latitude=[tup[1] for tup in Coordinate_List]

df = pd.DataFrame(list(zip(longitude, latitude)),
               columns =['latitude', 'longitude'])

# fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)

# fig = go.Figure(go.Scattermapbox(
#     mode = "markers",
#     lon = [longitude[0]], lat = [latitude[0]],
#     # data_frame=df,
#     marker = {'size': 20, 'symbol': ["airport"]}))

fig = go.Figure(go.Scattermapbox(
    mode = "markers+text",
    lon = df.longitude, lat = df.latitude,
    marker = {'size': 15, 'color': 'green', 'symbol': ["triangle-stroked" for i in range(len(longitude)+1)]}))

fig.update_layout(
    # height = 1200,
    mapbox = {
        'accesstoken': 'pk.eyJ1IjoianVhbmRhZyIsImEiOiJja3QzaGUzNWIwMXVxMm5sOWxvNjZsb2dtIn0.s_KuM7an3olAI8QxLRGKZA',
        'style': "streets", 'zoom': 4, 'center_lat': 4.29, 'center_lon': -74.82},
    showlegend = False)

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox={"style":"open-street-map"})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

map_app1.layout = html.Div([
    dcc.Graph(figure=fig)
])



