from server_flask import server

from flask import Flask, render_template
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd

## Apps
from apps.map_app import map_app1
from apps.gen_app import gen_app
from apps.balance_app import balance_app

#################

@server.route('/dashgen/')
def render_dashgen():
	return gen_app.index()


@server.route('/map_app/')
def render_dashmap():
    return map_app1.index()

@server.route('/dashbalance/')
def render_dashbalance():
	return balance_app.index()

@server.route('/')
def index():
    return render_template('context.html' )

# @server.route('/predict')
# def predict():
#     return render_template('predict.html' )

@server.route('/balance')
def predict():
    return render_template('balance.html' )
    # return balance_app.index()

@server.route('/gen')
def view_gen():
    return render_template('generation.html' )

@server.route('/consumption')
def view_consumption():
    return render_template('index.html' )

@server.route('/about')
def view_about():
    return render_template( 'about.html' )



if __name__ == '__main__':
    server.run( port='8080', debug = True )