from inspect import classify_class_attrs
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Shadow import Shadow
import pandas as pd
from dash import Dash
import plotly.express as px
import dash_bootstrap_components as dbc


# Server
from server_flask import server

# Connection to the database
from server_flask import con

# Data

query = 'SELECT * FROM '
DataList=[
# 'consumption'         ,
# 'forecasted_24months'  ,       
# 'ghi_2021_preds'      ,
'ghi_gen_preds',       
# 'ghi_generation',      
# 'locationmonthaverage',
'locationyearaverage', 
# 'wind_2021_preds' ,    
'wind_gen_preds'      
# 'windspeed' 
]

DataBase={Name:pd.read_sql(query+Name,con) for Name in DataList}

# query = 'SELECT * FROM consumption'
# consumption = pd.read_sql(query,con)

# Data Estaciones

# Coordinate_List = [

#     (18.49,-67.14),
#     (18.45,-66.18),
#     (10.41,-75.58),
#     (4.29,-74.82),
#     (9.73,-75.06),
#     (10.97,-73.54),
#     (9.73,-73.86),
#     (11.33,-72.74),
#     (8.53,-76.70),
#     (8.05,-75.18),
#     (8.77,-75.86),
#     (10.69,-74.86),
#     (10.49,-74.34),
#     (10.41,-75.58),
#     (8.93,-75.46),
#     (8.21,-76.38),
#     (9.17,-75.30),
#     (7.85,-76.82),
#     (6.73,-76.70),
#     (10.77,-73.98),
#     (8.37,-74.90),
#     (7.33,-75.78),
#     (9.05,-74.10),
#     (4.29,-74.82),
#     (10.45,-73.18),
#     (10.21,-74.90)
# ]

Coordinate_List = [
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



balance_app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP] , server = server, url_base_pathname='/dashbalance/')

balance_app.layout = html.Div(children=[
    html.H3(children='Mapa de calor de capacidad energética' ,style={"margin-bottom": "20px"}),
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
            
                ], className='mb-2 mt-1', width=8),
    ]),

    html.Div(children = [
        html.Iframe(src="http://127.0.0.1:8080/map_app", height="330px", width="60%" ,style={"position": "absolute", "margin": "20px 0 0 0"})
    ],
    style={
        'background-color': 'white',
        'height': '400px',
        'width': '100%'
    }),
    html.Div(children=[
        html.H3(children='Indicadores', style={'margin-bottom': '30px'}),
        dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Estación', style={
                                'color': 'white', }),
                        html.H2(id='estacion_val', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#0E9F6E'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=3, style={'text-align-last': 'center'}),
        
         dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Irradiancia media', style={
                                'color': 'white', }),
                        html.H2(id='irradiancia_media', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#0E9F6E'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=3, style={'text-align-last': 'center'}),
        
         dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Temperatura media', style={
                                'color': 'white', }),
                        html.H2(id='temp_media', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#0E9F6E'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=3, style={'text-align-last': 'center'}),

        dbc.Col([
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H6('Velocidad de viento media', style={
                                'color': 'white', }),
                        html.H2(id='viento_media', children="000", style={
                            'font-weight': 'bold', 'color': 'white'})
                    ], style={'textAlign': 'center', 'padding': '0.4rem'})
                ], style={'border-radius': '20px', 'background-color': '#0E9F6E'}),
            ], className='mr-2', style={'width': '70%', 'display': 'inline-block'})
        ], width=3, style={'text-align-last': 'center'}),
    ],className='mb-2', justify="end")
    ], style={'margin': '30px 0 0 0', 'background-color': 'white', 'height': '200px', 'width': '100%'}),

    #Selectors
    dbc.Row([
        dbc.Col([
            html.H3('Distribución de consumo en el hogar'),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                    
                    html.H4('Elige tu microred', className='card-title',
                             style={'color': '#2B3674', }),

                     html.Div([
                         dbc.Col([
                                 html.P(['Paneles solares'], style={
                                        'color': '#2B3674', })
                                 ], width=6),
                        dbc.Col([
                                 dcc.Dropdown(id='clase_panel',
                                            #   options=[{'label': i, 'value': str(
                                            #       i)} for i in range(1, 3)],
                                            options=[{'label': 'MSX60', 'value': 'Panel 1'}],
                                              placeholder="Clase",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                        
                         dbc.Col([
                                 dcc.Dropdown(id='cantidad_panel',
                                              options=[{'label': i, 'value': str(
                                                  i)} for i in range(1, 20)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                     html.Div([
                         dbc.Col([
                                 html.P(['Turbinas eólicas'], style={
                                        'color': '#2B3674', })
                                 ], width=6),

                        dbc.Col([
                                 dcc.Dropdown(id='clase_turbinas',
                                              options=[{'label': str(i)+" m" , 'value':i} for i in range(3, 8)],
                                              placeholder="Radio",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                    
                        
                         dbc.Col([
                                 dcc.Dropdown(id='cantidad_turbinas',
                                              options=[{'label': i, 'value': str(
                                                  i)} for i in range(1, 20)],
                                              placeholder="Cantidad",
                                              style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                                                     'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                                              ),
                                 ], width=3, style={'margin-left': 'auto'}),
                     ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                     html.Hr(style={'margin': '0'}),

                    #  html.Div([
                    #      dbc.Col([
                    #              html.P(['Región'], style={
                    #                     'color': '#2B3674', })
                    #              ], width=6),
                    #      dbc.Col([
                    #              dcc.Dropdown(id='region',
                    #                           options=[{'label': i, 'value': str(
                    #                               i)} for i in range(1, 10)],
                    #                           placeholder="Región",
                    #                           style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                    #                                  'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                    #                           ),
                    #              ], width=3, style={'margin-left': 'auto'}),
                    #  ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                    #  html.Hr(style={'margin': '0'}),

                    #  html.Div([
                    #      dbc.Col([
                    #          html.P(['Costo kWH'], style={
                    #              'color': '#2B3674', })
                    #      ], width=6),
                    #      dbc.Col([
                    #          dcc.Dropdown(id='costo_kwh',
                    #                       options=[{'label': i, 'value': str(
                    #                           i)} for i in range(1, 100)],
                    #                       placeholder="Precio",
                    #                       style={'font-size': '14px', 'white-space': 'nowrap', 'text-overflow': 'ellipsis',
                    #                              'border-radius': '8px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)', 'border-color': 'black'}
                    #                       ),
                    #      ], width=3, style={'margin-left': 'auto'}),
                    #  ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
                    #  html.Hr(style={'margin': '0'}),

                     ])
                ])
            ], style={'border-radius': '10px', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.1)'}),
        ], className='mb-3', width=6),
        # Second column
        dbc.Col([
            html.H3('Energía promedio mensual generada'),
            dbc.Card([
                dbc.CardBody([
                     dcc.Graph(id='line-generation-energy', figure={}, config={'displayModeBar': False}),                   
                ])
            ])
            
        ], className='mb-3', width=6),
    ], className='mt-4', justify="end"),


# Appliances table----------------------------------

# html.Div(children=[
#     html.H3(children='Tu microred'),
#     dbc.Row([
#         dbc.Col([
#             # html.Div([
#             #     html.H4('Content')
#             # ], style={'background-color': 'white', 'height': '100%'}),
#             dbc.Card([
#                 dbc.CardBody([
#                     html.Div([
#                         html.Div([
#                          dbc.Col([
#                                  html.H5(['Electrodomestico'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4),
#                         dbc.Col([
#                                  html.H5(['Potencia kW/H'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
                        
#                          dbc.Col([
#                                  html.H5(['Porcentaje'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
#                      ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
#                      html.Hr(style={'margin': '0'}),

#                      html.Div([
#                          dbc.Col([
#                                  html.P(['Nevera'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4),
#                         dbc.Col([
#                                  html.P(['200 W'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
                        
#                          dbc.Col([
#                                  html.P(['20%'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
#                      ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
#                      html.Hr(style={'margin': '0'}),

#                      html.Div([
#                          dbc.Col([
#                                  html.P(['Nevera'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4),
#                         dbc.Col([
#                                  html.P(['200 W'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
                        
#                          dbc.Col([
#                                  html.P(['20%'], style={
#                                         'color': '#2B3674', })
#                                  ], width=4, style={'margin-left': 'auto'}),
#                      ], className='mr-2 mb-1 mt-1', style={'width': '100%', 'display': 'flex'}),
#                      html.Hr(style={'margin': '0'}),


#                     ])
#                 ])
#             ])

#             ], width=12, style={'text-align-last': 'left'})

#     ], className='mb-2 mt-1', style={"height": "100%"})
# ], style={'background-color': 'white', 'width': '100%', "height": '350px'}),


# End Appliances table----------------------------------

# Footer
    dbc.Row([
        dbc.Col([
            html.Footer([
                html.P('© 2021 Copyright: Green Watts', className='text-center text-lg-start text-muted',
                             style={'background':"rgba(0, 0, 0, 0.05)", 'padding':'1.5rem','font-size':'.875rem', 'border-radius': '10px'  })
                    ], style={"background-color": "rgba(0, 0, 0, 0.05)"})
                ], width=12),
    ],className='mb-2 mt-2',  justify="end"),

# html.Div(children=[
#     html.H3('Tu microred', style={'color': 'black'})
# ], style={'background-color': 'white', 'width': '100%', "height": '400px'})
], style={'margin': '30px 0 0 30px', "background-color": "white"})  
# ], style={'margin': '30px 0 0 30px'})


# UPDATE INDICADORES--------------------------
@balance_app.callback(
    Output('estacion_val', 'children'),
    Output('irradiancia_media', 'children'),
    Output('temp_media', 'children'),
    Output('viento_media', 'children'),
    Input('estacion_dropdown', 'value'),
)

def update_indicators(estacion_dropdown):

    estacion = estacion_dropdown
    locationyearaverage_df = DataBase["locationyearaverage"]
    irradiancia_media = str(round(locationyearaverage_df.loc[locationyearaverage_df["longitude_latitude"] == str(estacion_dropdown)].ghi.mean(), 3)) + " W/m²"
    temp_media = str(round(locationyearaverage_df.loc[locationyearaverage_df["longitude_latitude"] == str(estacion_dropdown)].temperature.mean(),3)) + " °C"
    viento_media = str(round(locationyearaverage_df.loc[locationyearaverage_df["longitude_latitude"] == str(estacion_dropdown)].wind_speed.mean(), 3)) + " m/s"

    return estacion, irradiancia_media, temp_media, viento_media


Modelos_Dict={'Regresión Lineal Horizontal':
                                    {"Min":"2021-01-01 00:00:00",
                                     "Max":"2021-12-31 23:00:00",
                                     "freq":"H",
                                     "Solar":DataBase["ghi_gen_preds"],
                                     "Eólica":DataBase["wind_gen_preds"]}
                # "ARIMA":
                #                     {"Min":"2021-01-01 00:00:00",
                #                      "Max":"2022-12-31 23:00:00",
                #                      "freq":"M",
                #                      "Solar":DataBase["forecasted_24months"][DataBase["forecasted_24months"]["variable"]=="GHI"],
                #                      "Eólica":DataBase["forecasted_24months"][DataBase["forecasted_24months"]["variable"]=="Wind Speed"]}
                }

DataBase["ghi_gen_preds"].columns=["id","(4.29, -74.82) 2021 GHI","(6.73, -76.7) 2021 GHI","(7.33, -75.78) 2021 GHI","(7.85, -76.82) 2021 GHI","(8.05, -75.18) 2021 GHI","(8.21, -76.38) 2021 GHI","(8.37, -74.9) 2021 GHI","(8.53, -76.7) 2021 GHI","(8.77, -75.86) 2021 GHI","(8.93, -75.46) 2021 GHI","(9.05, -74.1) 2021 GHI","(9.17, -75.3) 2021 GHI","(9.73, -75.06) 2021 GHI","(9.73, -73.86) 2021 GHI","(10.21, -74.9) 2021 GHI","(10.41, -75.58) 2021 GHI","(10.45, -73.18) 2021 GHI","(10.49, -74.34) 2021 GHI","(10.69, -74.86) 2021 GHI","(10.77, -73.98) 2021 GHI","(10.97, -73.54) 2021 GHI","(11.33, -72.74) 2021 GHI","datetime"]
# print(DataBase["ghi_gen_preds"].columns)
DataBase["wind_gen_preds"].columns=["id","(4.29, -74.82) 2021 Wind Speed","(6.73, -76.7) 2021 Wind Speed","(7.33, -75.78) 2021 Wind Speed","(7.85, -76.82) 2021 Wind Speed","(8.05, -75.18) 2021 Wind Speed","(8.21, -76.38) 2021 Wind Speed","(8.37, -74.9) 2021 Wind Speed","(8.53, -76.7) 2021 Wind Speed","(8.77, -75.86) 2021 Wind Speed","(8.93, -75.46) 2021 Wind Speed","(9.05, -74.1) 2021 Wind Speed","(9.17, -75.3) 2021 Wind Speed","(9.73, -75.06) 2021 Wind Speed","(9.73, -73.86) 2021 Wind Speed","(10.21, -74.9) 2021 Wind Speed","(10.41, -75.58) 2021 Wind Speed","(10.45, -73.18) 2021 Wind Speed","(10.49, -74.34) 2021 Wind Speed","(10.69, -74.86) 2021 Wind Speed","(10.77, -73.98) 2021 Wind Speed","(10.97, -73.54) 2021 Wind Speed","(11.33, -72.74) 2021 Wind Speed","datetime"]


# UPDATE GRAFICA ENERGIA PROMEDIO--------------------------

@balance_app.callback(
    Output('line-generation-energy', 'figure'),
    Input('estacion_dropdown', 'value'),
    Input('clase_panel', 'value'),
    Input('cantidad_panel', 'value'),
    Input('clase_turbinas', 'value'),
    Input('cantidad_turbinas', 'value'),
    # Input('region', 'value'),
    # Input('costo_kwh', 'value'),
)

def update_energy_graph(estacion_dropdown,
        clase_panel,
        cantidad_paneles,
        clase_turbinas,
        cantidad_turbinas
        # region,
        # costo_kwh
        ):

    #FUNCTIONTODO ----

    data_type={"Eólica":"Wind Speed","Solar":"GHI"}
    cantidades={"Eólica":cantidad_turbinas,"Solar":cantidad_paneles}
    estacion_dropdown1_solar=str(estacion_dropdown)+" 2021 "+data_type["Solar"]
    estacion_dropdown1_eolica=str(estacion_dropdown)+" 2021 "+data_type["Eólica"]
    
    modelo_dropdown, energia_solar, energia_eolica = "Regresión Lineal Horizontal", "Solar", "Eólica"
    data_gen_solar =Modelos_Dict[modelo_dropdown][energia_solar][estacion_dropdown1_solar]
    data_gen_eolica =Modelos_Dict[modelo_dropdown][energia_eolica][estacion_dropdown1_eolica]
    
    total_gen_solar = data_gen_solar.astype("float").apply(lambda x:x*int(cantidad_paneles)).mean()
    total_gen_eolica = data_gen_eolica.astype("float").apply(lambda x:x*int(cantidad_turbinas)*((int(clase_turbinas)**2)/(5**2))).mean()
    
    # total_gen_solar = 23.0
    # total_gen_eolica = 22.0

    # if modelo_dropdown=="Regresión Lineal Horizontal":
    #     data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][estacion_dropdown1]
    #     if energia_dropdown=="Eólica":
    #         total_gen=data_gen.astype("float").apply(lambda x:x*turbinas_cantidad*((int(tipo_turbina)**2)/(5**2))).mean()
    #     else:
    #         total_gen=data_gen.astype("float").apply(lambda x:x*paneles_cantidad).mean()
    # else:
    #     data_gen=Modelos_Dict[modelo_dropdown][energia_dropdown][(Modelos_Dict[modelo_dropdown][energia_dropdown]["variable"]==data_type[energia_dropdown])&(Modelos_Dict[modelo_dropdown][energia_dropdown]["location"]==estacion_dropdown)]
    #     total_gen=data_gen["values"].astype("float").mean()
    # consumo_columnas=["id","datetime","JFP_1 (kWhs)","JFP_2 (kWhs)","room outlets (kWhs)","Heater  (kWhs)","Hall Light (kWhs)","Oven (kWhs)","Family Light (kWhs)","Fridge (kWhs)","Washer/Dryer (kWhs)","Fam Outlets (kWhs)"]
    # lista_cantidades=[0,0,toma_corrientes,0,tomas_cuartos,calefaccion,bombillas,horno,5,nevera,lavadora,tomas_sala]
    # consumo=DataBase["consumption"]   
    # # print(consumo.dtypes)
    
    # consumo.columns=consumo_columnas
    # variables_dict=dict(zip(consumo_columnas,lista_cantidades))
    # consumos=[(variables_dict[columna])*(consumo[columna].astype("float").mean()) for columna in consumo_columnas[2:]]  
    # total_eng=round((sum(consumos)*30.0*24.0),3)
    total_gen_solar = round((total_gen_solar*24.0*30.0)/1000,3)
    total_gen_eolica = round((total_gen_eolica*24.0*30.0)/1000,3)
    fig_line_energy = px.bar(x=['Solar', 'Eolica'], y=[total_gen_solar, total_gen_eolica], labels={'x': 'Tipo de energía', 'y': 'Energía (kW)'})

    return fig_line_energy
    