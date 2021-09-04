from flask import Flask, render_template#, request, redirect, url_for, flash

import pandas as pd

from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


# Testing DB

from sqlalchemy import create_engine
from flask_migrate import Migrate

######################

server = Flask( __name__ )

# DB Connection
# ESPECIFY YOUR DB CONNECTION
# url = ""
# con = create_engine(url)

#################
