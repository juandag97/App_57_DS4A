from inspect import classify_class_attrs
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Shadow import Shadow
import pandas as pd
from dash import Dash
import plotly.express as px
# import plotly.graph_objs as go
import dash_bootstrap_components as dbc


# Server
from server_flask import server

# Connection to the database
from server_flask import con

# Data - Llamar una unica vez la base de datos
query = 'SELECT * FROM '
DataList=[
'consumption'         ,
'forecasted_24months'  ,       
# 'ghi_2021_preds'      ,
'ghi_gen_preds',       
# 'ghi_generation',      
'locationmonthaverage',
# 'locationyearaverage', 
# 'wind_2021_preds' ,    
'wind_gen_preds'   ,   
'windspeed' ]
DataBase={Name:pd.read_sql(query+Name,con) for Name in DataList}


# Data Estaciones
Coordinate_List = [
    # "(18.49, -67.14)",
    # "(18.45, -66.18)",
    "(10.41, -75.58)",
    "(4.29, -74.82)",
    "(9.73, -75.06)",
    "(10.97, -73.54)",
    "(9.73, -73.86)",
    "(11.33, -72.74)",
    "(8.53, -76.70)",
    "(8.05, -75.18)",
    "(8.77, -75.86)",
    "(10.69, -74.86)",
    "(10.49, -74.34)",
    "(10.41, -75.58)",
    "(8.93, -75.46)",
    "(8.21, -76.38)",
    "(9.17, -75.3)",
    "(7.85, -76.82)",
    "(6.73, -76.7)",
    "(10.77, -73.98)",
    "(8.37, -74.9)",
    "(7.33, -75.78)",
    "(9.05, -74.1)",
    "(10.45, -73.18)",
    "(10.21, -74.9)"
]
print("Data imports ready")

gen_app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP] , server = server, url_base_pathname='/dashgen/')

gen_app.layout = dbc.Container([
    # Dropdowns
    dbc.Row([

        dbc.Col([
            html.Div([
                dcc.Dropdown(id='estacion_dropdown',
                             options=[{'label': i, 'value': str(
                                 i)} for i in Coordinate_List],
                             placeholder="Estación Meteorológica",
                             style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                    'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                             ),
            ], className='mr-2', style={'width': '23%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(id='energia_dropdown',
                             options=[
                                 {'label': 'Eólica', 'value': 'Eólica'},
                                 {'label': 'Solar', 'value': 'Solar'}
                             ],
                             placeholder="Tipo de Energía",
                             style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                    'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                             ),
            ], className='mr-2', style={'width': '20%', 'display': 'inline-block'}
            ),
                        html.Div([
            dcc.Dropdown(id = 'modelo_dropdown',
                         options = [
                             {'label': 'ARIMA', 'value': 'ARIMA'},
                             {'label': 'Regresión Lineal', 'value': 'Regresión Lineal Horizontal'}
                             ],
                         placeholder = "Modelo",
                         style = {'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis', 'border-radius':'8px', 'box-shadow':'0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color':'black'}
                                     ),                            
                    ], className = 'mr-2', style={'width': '30%', 'display': 'inline-block'}
                    ),
                ], className='mb-2 mt-1', width=8),
    ]),
    # Alert
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Alert("Esta gráfica presenta los resultados para algunos modelos de generación de energía. Es importante clarificar que con el modelo ARIMA se alcanza una proyección de dos años con una granularidad de meses; con el modelo de regresión lineal horizontal se alcanza una proyección un año con una granularidad de una hora", color="warning"),
                    ])
                ], width=12),
    ],className='mb-2 mt-2',  justify="end"),
    # Alert2
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Alert("Modelo ARIMA - 24 meses desde ultima observacion con cadencia mensual", color="primary"),
                    ])
                ], width=12),
    ],className='mb-2 mt-2',  justify="end"),
    # Alert3
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Alert("Modelo de regresion lineal - 12 meses con cadencia de horas", color="primary"),
                    ])
                ], width=12),
    ],className='mb-2 mt-2',  justify="end"),
    # Figure
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='line-generation', figure={}, config={'displayModeBar': False}),                   
                ])
            ]),


        ], width=12),
    ], className='mb-2 mt-2',  justify="end"),
    # Cards
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Cuenta de energía KWh (Mensual)' , style={
                                'color': 'white', }),
                        html.H2(id='cuenta_energia', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#DC2F39'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=4, style={'text-align-last': 'center'}),
        
         dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Energía generada KWh (Mensual)', style={
                                'color': 'white', }),
                        html.H2(id='energia_generada', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#47548C'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=4, style={'text-align-last': 'center'}),
        
         dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Ahorro $ (Mensual)', style={
                                'color': 'white', }),
                        html.H2(id='ahorro', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#0E9F6E'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=4, style={'text-align-last': 'center'}),
    ],className='mb-2', justify="end"),
    #Selectors
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                     html.H6('Elige tus electrodomésticos', className='card-title',
                             style={'color': '#2B3674', }),

                     html.Div([
                         dbc.Col([
                                 html.P(['Toma corrientes'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='toma_corrientes',
                                              options=[{'label': i, 'value': i} for i in range(10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                                 html.P(['Horno'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='horno',
                                              options=[{'label': i, 'value':i} for i in range(10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                                 html.P(['Nevera'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='nevera',
                                              options=[{'label': i, 'value':i} for i in range(10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                                 html.P(['Calefaccion'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='calefaccion',
                                              options=[{'label': i, 'value': i} for i in range(10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Lavadora-Secadora'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([
                             dcc.Dropdown(id='lavadora',
                                          options=[{'label': i, 'value':i} for i in range(10)],
                                          placeholder="Cantidad",
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Tomacorrientes Cuartos'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([
                             dcc.Dropdown(id='tomas_cuartos',
                                          options=[{'label': i, 'value':i} for i in range(10)],
                                          placeholder="Cantidad",
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Ventiladores'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([
                             dcc.Dropdown(id='ventiladores',
                                          options=[{'label': i, 'value': i} for i in range(10)],
                                          placeholder="Cantidad",
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Tomacorrientes Sala'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([
                             dcc.Dropdown(id='tomas_sala',
                                          options=[{'label': i, 'value':i} for i in range(10)],
                                          placeholder="Cantidad",
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Bombillas en espacios comunes'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([
                             dcc.Dropdown(id='bombillas',
                                          options=[{'label': i, 'value': i} for i in range(10)],
                                          placeholder="Cantidad",
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     ])
                ])
            ], style={'border-radius': '10px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)'}),
        ], className='mb-3', width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                     html.H6('Arma tu microred', className='card-title',
                             style={'color': '#2B3674', }),

                     html.Div([
                         dbc.Col([
                                 html.P(['Turbinas eólicas'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='tipo_turbina',
                                            #   options=[{'label': str(i+3)+" m" , 'value':i+3} for i in range(5)],
                                              options=[{'label': str(i)+" m" , 'value':i} for i in range(3, 8)],
                                              placeholder="Radio",
                                              style={'font-size': '14px','margin-bottom': '7px','white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                              
                                 dcc.Dropdown(id='turbinas_cantidad',
                                              options=[{'label': i, 'value':i} for i in range(0, 10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                              
                                 ], width=6, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                                 html.P(['Paneles solares'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                         dbc.Col([
                                 dcc.Dropdown(id='tipo_panel',
                                              options=[{'label': 'MSX60', 'value': 'Panel 1'}],
                                              placeholder="Tipo",
                                              style={'font-size': '14px','margin-bottom': '7px','white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                              
                                 dcc.Dropdown(id='paneles_cantidad',
                                              options=[{'label': i, 'value':i} for i in range(0, 10)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                              
                                 ], width=6, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                             html.P(['Costo kWh'], style={
                                 'color': '#2B3674', })
                         ], width=6),
                         dbc.Col([                                    
                             dcc.Input(id='costokwh',
                                            type="number",
                                          placeholder=6000.0,
                                          style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                 'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                          ),
                         ], width=6, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     ])
                ])
            ], style={'border-radius': '10px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)'}),
        ], className='mb-3', width=6),
    ], className='mt-4', justify="end"),
    # Footer
    dbc.Row([
        dbc.Col([
            html.Footer([
                html.P('© 2021 Copyright: Green Watts', className='text-center text-lg-start text-muted',
                             style={'background':'white', 'padding':'1.5rem','font-size':'.875rem', 'border-radius': '10px'  })
                    ])
                ], width=12),
    ],className='mb-2 mt-2',  justify="end"),




], fluid=True, className='mt-10', style={'backgroundColor': '#F9FAFB'})

Modelos_Dict={'Regresión Lineal Horizontal':
                                    {"Min":"2021-01-01 00:00:00",
                                     "Max":"2021-12-31 23:00:00",
                                     "freq":"H",
                                     "Solar":DataBase["ghi_gen_preds"],
                                     "Eólica":DataBase["wind_gen_preds"]},
                "ARIMA":
                                    {"Min":"2021-01-01 00:00:00",
                                     "Max":"2022-12-31 23:00:00",
                                     "freq":"H",
                                     "Solar":DataBase["forecasted_24months"][DataBase["forecasted_24months"]["variable"]=="GHI"],
                                     "Eólica":DataBase["forecasted_24months"][DataBase["forecasted_24months"]["variable"]=="Wind Speed"]}}

DataBase["ghi_gen_preds"].columns=["id","(4.29, -74.82) 2021 GHI","(6.73, -76.7) 2021 GHI","(7.33, -75.78) 2021 GHI","(7.85, -76.82) 2021 GHI","(8.05, -75.18) 2021 GHI","(8.21, -76.38) 2021 GHI","(8.37, -74.9) 2021 GHI","(8.53, -76.7) 2021 GHI","(8.77, -75.86) 2021 GHI","(8.93, -75.46) 2021 GHI","(9.05, -74.1) 2021 GHI","(9.17, -75.3) 2021 GHI","(9.73, -75.06) 2021 GHI","(9.73, -73.86) 2021 GHI","(10.21, -74.9) 2021 GHI","(10.41, -75.58) 2021 GHI","(10.45, -73.18) 2021 GHI","(10.49, -74.34) 2021 GHI","(10.69, -74.86) 2021 GHI","(10.77, -73.98) 2021 GHI","(10.97, -73.54) 2021 GHI","(11.33, -72.74) 2021 GHI","datetime"]
# print(DataBase["ghi_gen_preds"].columns)
DataBase["wind_gen_preds"].columns=["id","(4.29, -74.82) 2021 Wind Speed","(6.73, -76.7) 2021 Wind Speed","(7.33, -75.78) 2021 Wind Speed","(7.85, -76.82) 2021 Wind Speed","(8.05, -75.18) 2021 Wind Speed","(8.21, -76.38) 2021 Wind Speed","(8.37, -74.9) 2021 Wind Speed","(8.53, -76.7) 2021 Wind Speed","(8.77, -75.86) 2021 Wind Speed","(8.93, -75.46) 2021 Wind Speed","(9.05, -74.1) 2021 Wind Speed","(9.17, -75.3) 2021 Wind Speed","(9.73, -75.06) 2021 Wind Speed","(9.73, -73.86) 2021 Wind Speed","(10.21, -74.9) 2021 Wind Speed","(10.41, -75.58) 2021 Wind Speed","(10.45, -73.18) 2021 Wind Speed","(10.49, -74.34) 2021 Wind Speed","(10.69, -74.86) 2021 Wind Speed","(10.77, -73.98) 2021 Wind Speed","(10.97, -73.54) 2021 Wind Speed","(11.33, -72.74) 2021 Wind Speed","datetime"]
# print(DataBase["wind_gen_preds"].columns)
# Updating Line Plot******************************************
@gen_app.callback(
    Output('line-generation','figure'),
    Input('estacion_dropdown','value'),
    Input('energia_dropdown','value'),
    Input('modelo_dropdown','value'),
    Input('toma_corrientes','value'),
    Input('horno','value'),
    Input('nevera','value'),
    Input('calefaccion','value'),
    Input('lavadora','value'),
    Input('tomas_cuartos','value'),
    Input('ventiladores','value'),
    Input('tomas_sala','value'),
    Input('bombillas','value'),
    Input('tipo_turbina','value'),
    Input('turbinas_cantidad','value'),
    Input('paneles_cantidad','value'),
    Input('costokwh','value')
)
def update_graphs(
    estacion_dropdown,  #Tupla coordenadas
    energia_dropdown,   #"Eólica" o "Solar"
    modelo_dropdown,    #"ARIMA" o "Regresion lineal horizontal"
    toma_corrientes,    #int
    horno,              #int
    nevera,             #int
    calefaccion,        #int
    lavadora,           #int
    tomas_cuartos,      #int
    ventiladores,       #int
    tomas_sala,         #int
    bombillas,          #int
    tipo_turbina,       #int
    turbinas_cantidad,
    paneles_cantidad,
    costokwh):
    #float
    # inputs=locals()
    # for tag in inputs:
    #     if type(inputs[tag])==type(None):
    #         inputs[tag]=0
    data_type={"Eólica":"Wind Speed","Solar":"GHI"}
    cantidades={"Eólica":turbinas_cantidad,"Solar":paneles_cantidad}
    estacion_dropdown1=str(estacion_dropdown)+" 2021 "+data_type[energia_dropdown]
    if modelo_dropdown=="Regresión Lineal Horizontal":
        # print(Modelos_Dict[modelo_dropdown]["Min"])
        X_values=pd.date_range(Modelos_Dict[modelo_dropdown]["Min"],
                            Modelos_Dict[modelo_dropdown]["Max"],
                            freq=Modelos_Dict[modelo_dropdown]["freq"])
        
        data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][estacion_dropdown1]
        if energia_dropdown=="Eólica":
            # print(type(turbinas_cantidad))
            Y_values=data_gen.astype("float").apply(lambda x:x*turbinas_cantidad*tipo_turbina*tipo_turbina/25.0)
        else:
            # print(type(paneles_cantidad))
            Y_values=data_gen.astype("float").apply(lambda x:x*paneles_cantidad)
    else:
        X_values1=pd.date_range(Modelos_Dict[modelo_dropdown]["Min"],
                            Modelos_Dict[modelo_dropdown]["Max"],
                            freq=Modelos_Dict[modelo_dropdown]["freq"])
        print(Modelos_Dict[modelo_dropdown][energia_dropdown].columns)
        data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][Modelos_Dict[modelo_dropdown][energia_dropdown]["variable"]==data_type[energia_dropdown]][Modelos_Dict[modelo_dropdown][energia_dropdown]["location"]==estacion_dropdown]
        if energia_dropdown=="Eólica":
            Y_values1=Modelos_Dict[modelo_dropdown][energia_dropdown]["values"].astype("float").apply(lambda x:x*turbinas_cantidad*tipo_turbina*tipo_turbina/25.0)
        else:
            Y_values1=Modelos_Dict[modelo_dropdown][energia_dropdown]["values"].astype("float").apply(lambda x:x*paneles_cantidad)
        newYValues=[]
        for date in X_values1:
            if date.year==2020:
                newYValues.append(Y_values1.iloc[date.month])
            else:
                newYValues.append(Y_values1.iloc[date.month+12])
    consumo_columnas=["id","datetime","JFP_1 (kWhs)","JFP_2 (kWhs)","room outlets (kWhs)","Heater  (kWhs)","Hall Light (kWhs)","Oven (kWhs)","Family Light (kWhs)","Fridge (kWhs)","Washer/Dryer (kWhs)","Fam Outlets (kWhs)"]
    lista_cantidades=[0,0,toma_corrientes/2.0,toma_corrientes/2.0,tomas_cuartos,calefaccion,bombillas,horno,5,nevera,lavadora,tomas_sala]
    consumo=DataBase["consumption"]   
    # print(consumo.dtypes)
    
    consumo.columns=consumo_columnas
    variables_dict=dict(zip(consumo_columnas,lista_cantidades))
    consumos=[float(variables_dict[columna])*consumo[columna].mean() for columna in consumo_columnas[2:]]  
    Consumo_total=sum(consumos) 
    if modelo_dropdown=="Regresión Lineal Horizontal":
        fig_line=px.line(y=Y_values,x=X_values)
        fig_lineCON=px.line(y=[Consumo_total,Consumo_total],x=[X_values.min(),X_values.max()])
        fig_line.add_trace(fig_lineCON.data[0]) 
        return fig_line
    else:
        fig_line2=px.scatter(y=newYValues,x=X_values1)
        fig_lineCON1=px.line(y=[Consumo_total,Consumo_total],x=[X_values1.min(),X_values1.max()])
        fig_line2.add_trace(fig_lineCON1.data[0]) 
        return fig_line2


# Updating Cards******************************************
@gen_app.callback(
    Output('cuenta_energia','children'),
    Output('energia_generada','children'),
    Output('ahorro','children'),
    Input('estacion_dropdown','value'),
    Input('energia_dropdown','value'),
    Input('modelo_dropdown','value'),
    Input('toma_corrientes','value'),
    Input('horno','value'),
    Input('nevera','value'),   
    Input('calefaccion','value'),
    Input('lavadora','value'),
    Input('tomas_cuartos','value'),
    Input('ventiladores','value'),
    Input('tomas_sala','value'),
    Input('bombillas','value'),
    Input('tipo_turbina','value'),
    Input('turbinas_cantidad','value'),
    Input('paneles_cantidad','value'),
    Input('costokwh','value')
)
def update_small_cards(
    estacion_dropdown,
    energia_dropdown,
    modelo_dropdown,
    toma_corrientes,
    horno,
    nevera,
    calefaccion,
    lavadora,
    tomas_cuartos,
    ventiladores,
    tomas_sala,
    bombillas,
    tipo_turbina,
    turbinas_cantidad,
    paneles_cantidad,
    costokwh
    ):
    data_type={"Eólica":"Wind Speed","Solar":"GHI"}
    cantidades={"Eólica":turbinas_cantidad,"Solar":paneles_cantidad}
    estacion_dropdown1=str(estacion_dropdown)+" 2021 "+data_type[energia_dropdown]
    if modelo_dropdown=="Regresión Lineal Horizontal":
        data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][estacion_dropdown1]
        if energia_dropdown=="Eólica":
            total_gen=data_gen.astype("float").apply(lambda x:x*turbinas_cantidad*((int(tipo_turbina)**2)/(5**2))).mean()
        else:
            total_gen=data_gen.astype("float").apply(lambda x:x*paneles_cantidad).mean()
    else:
        if energia_dropdown=="Eólica":
            data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][(Modelos_Dict[modelo_dropdown][energia_dropdown]["variable"]==data_type[energia_dropdown])&(Modelos_Dict[modelo_dropdown][energia_dropdown]["location"]==estacion_dropdown)]
            total_gen=data_gen["values"].astype("float").apply(lambda x:x*turbinas_cantidad*((int(tipo_turbina)**2)/(5**2))).mean()
        else:
            data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][(Modelos_Dict[modelo_dropdown][energia_dropdown]["variable"]==data_type[energia_dropdown])&(Modelos_Dict[modelo_dropdown][energia_dropdown]["location"]==estacion_dropdown)]
            total_gen=data_gen["values"].astype("float").apply(lambda x:x*paneles_cantidad).mean()  
    consumo_columnas=["id","datetime","JFP_1 (kWhs)","JFP_2 (kWhs)","room outlets (kWhs)","Heater  (kWhs)","Hall Light (kWhs)","Oven (kWhs)","Family Light (kWhs)","Fridge (kWhs)","Washer/Dryer (kWhs)","Fam Outlets (kWhs)"]
    lista_cantidades=[0,0,toma_corrientes/2.0,toma_corrientes/2.0,tomas_cuartos,calefaccion,bombillas,horno,5,nevera,lavadora,tomas_sala]
    consumo=DataBase["consumption"]   
    # print(consumo.dtypes)
    
    consumo.columns=consumo_columnas
    variables_dict=dict(zip(consumo_columnas,lista_cantidades))
    consumos=[(variables_dict[columna])*(consumo[columna].astype("float").mean()) for columna in consumo_columnas[2:]]  
    total_eng=round((sum(consumos)*30.0*24.0),3)
    total_gen=round((total_gen*24.0*30.0),3)
    # try:
    #     c=[]
    #     numb=[]
    #     for i in range(len(costokwh)):
    #         numb.append(float(costokwh[i]))
    #     a=len(costokwh)
    #     newcost=sum([numb[i]*10**(a-i) for i in range(a)])
    #     print(type(newcost))
    # except:
    #     print(type(costokwh))
    if total_gen<=0:
        total_gen=0
    total_ahorronumb=round((-total_eng+total_gen)*costokwh,3)
    total_ahorro='$'+f'{total_ahorronumb:,}'+'.00'
    return total_eng, total_gen, total_ahorro