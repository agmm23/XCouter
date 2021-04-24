# Imports
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlalchemy as sql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from copy import deepcopy
import flask
import plotly.express as px
import timeit

from functions import draw_plotly_fiba_court, transform_coordinates, distancia_aro, create_hexagons, define_section,\
    calculate_succes_per_section, calculate_freq_x_hex, add_traces_to_court, recibir_df_y_calcular_hexagonos, \
    calcular_Hexagonos_y_frecuenciasxEquipo, calcular_Hexagonos_y_frecuenciaxJugador_Tirador, calcular_puntos, \
    pbp_player_in_field, pbp_player_not_in_field


# region Variables Declaration

Court_width = 1500
Court_height = 1400
threept_break_y = 300
three_area = 675


# endregion


# region Conectar a base de datos y traer a un dataframe
connect_string = 'mysql+mysqlconnector://root:password@localhost:3306/xcouter_2021'

sql_engine = sql.create_engine(connect_string)
query = "select * from playbyplay" #Todo Cambiar la query por una de alchemy

df = pd.read_sql_query(query, sql_engine)

df_shots = df[['id_match', 'actionType_x', 'player_x', 'success', 'team_name', 'team_rival', 'x', 'y',
               'Player_1_Name_Home', 'Player_2_Name_Home', 'Player_3_Name_Home', 'Player_4_Name_Home', 'Player_5_Name_Home',
               'Player_1_Name_Away', 'Player_2_Name_Away', 'Player_3_Name_Away', 'Player_4_Name_Away', 'Player_5_Name_Away']]
df_shots = df_shots[df_shots['actionType_x'].isin(['2pt', '3pt'])]
# endregion

#ASISTENCIAS
df_assists = deepcopy(df)
df_assists['points'] = df_assists.apply(lambda x:calcular_puntos(x), axis=1)

playbyplay_points = df_assists[df_assists['points']>0]
pointsperplayer = pd.DataFrame()

#Preparacion de datos para el scatter plot de asistencias
pointsperplayer['assisted'] = playbyplay_points[playbyplay_points['Complementary_player'].notnull()].groupby(['player_x','team_name'])['points'].sum()
# pointsperplayer['not_assisted'] = playbyplay_points[playbyplay_points['Complementary_player']=='0'].groupby(['player_x','team_name'])['points'].sum()
pointsperplayer['not_assisted'] = playbyplay_points[playbyplay_points['Complementary_player'].isnull()].groupby(['player_x','team_name'])['points'].sum()
pointsperplayer.reset_index(inplace=True)
pointsperplayer.fillna(0, inplace=True)


# Manipulacion del dataframe (convertir columnas y calculos)
# Generar nuevas coordenadas
df_shots['temporary'] = df_shots.apply(lambda a: transform_coordinates(a['x'], a['y'], 0, 0, 0, 'left', 'bottom'),
                                       axis=1)
df_shots['x_converted'] = df_shots['temporary'].apply(lambda x: x[0])
df_shots['y_converted'] = df_shots['temporary'].apply(lambda x: x[1])
df_shots.drop('temporary', axis=1, inplace=True)

# Agregar distancia
df_shots['distance'] = df_shots.apply(lambda a: distancia_aro(a['x_converted'], a['y_converted']), axis=1)

# Asignar area de tiro a cada tiro
df_shots['shot_section'] = df_shots.apply(lambda a: define_section(a['x_converted'], a['y_converted'], a['distance']),
                                          axis=1)
# endregion


# region Crear hexagonos para la liga
hex_stats_league = create_hexagons(df_shots)
hex_stats_league['distance'] = hex_stats_league.apply(lambda a: distancia_aro(a['x'], a['y']), axis=1)
hex_stats_league['shot_section'] = hex_stats_league.apply(lambda a: define_section(a['x'], a['y'], a['distance']),
                                                          axis=1)
hex_stats_league = calculate_succes_per_section(hex_stats_league)
base_hexbin_stats = deepcopy(hex_stats_league)
# endregion


# Aplicacion Dash
# Obtener todas las opciones posibles de equipo
all_teams = sorted(df['team_name'].unique().tolist())

# Obtengo todos los equipos
all_team_players = df.groupby('team_name')['player_x'].unique().apply(list).to_dict()

# A cada set de jugadores por equipo le agrego la opcion All
for k, v in all_team_players.items():
    all_team_players[k].insert(0, 'ALL')

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/dash/')

app.layout = html.Div([
    html.Div([
        html.H1('Equipo Local'),
        dcc.Dropdown(
            id='dropdown-team-local',
            options=[{'label': k, 'value': k} for k in all_team_players.keys()],
            value=all_teams[0]
        )], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        html.H1('Equipo Rival'),
        dcc.Dropdown(
            id='dropdown-team-rival',
            options=[{'label': k, 'value': k} for k in all_team_players.keys()],
            value=all_teams[0]
        )], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.H1('Ofensiva Local'),
        dcc.Graph(id='graph-court-off')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Defensa Rival'),
        dcc.Graph(id='graph-court-def-rival')
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Defensa Local'),
        dcc.Graph(id='graph-court-def')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Ofensiva Rival'),
        dcc.Graph(id='graph-court-off-rival')
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Asistencias')
    ]),
    html.Div([
        html.H2('Grafico 1'),
        dcc.Graph(id='graph-scatter-assists')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H2('Grafico 2'),
        dcc.Graph(id='graph-parcat-assists')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H2('Grafico 3'),
        dcc.Graph(id='graph-sunburst-assists')
    ]),
    html.Div([
        html.H2('Jugador Local'),
        dcc.Dropdown(
            id='dropdown-player-local',
            value='ALL'),
    ]
    ),
    html.Div([
        html.H1('Jugador Local'),
        dcc.Graph(id='graph-court-local-player')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Tiros del equipo CON el jugador en cancha'),
        dcc.Graph(id='graph-court-local-player_in_field')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Tiros del equipo SIN el jugador en cancha'),
        dcc.Graph(id='court_team_shots_player_not_in_field')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Defensa del equipo CON el jugador en cancha'),
        dcc.Graph(id='court_team_defense_player_in_field')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Defensa del equipo SIN el jugador en cancha'),
        dcc.Graph(id='court_team_defense_player_not_in_field')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    #TODO Como defiende el equipo CON el jugador en cancha
    #TODO Como defiende el equipo SIN el jugador en cancha
]
)

#EQUIPO LOCAL
@app.callback(
    [Output('graph-court-off', 'figure'), Output('graph-court-def', 'figure'),
     Output('graph-scatter-assists', 'figure'), Output('graph-parcat-assists', 'figure'), Output('graph-sunburst-assists', 'figure')],
    [Input('dropdown-team-local', 'value')])

def update_figure(selected_team_rel):
    # OFENSIVA
    # Crea hexagonos para el equipo seleccionado y calcula las estadisticas para esos hexagonos

    rel_hexbin_stats = calcular_Hexagonos_y_frecuenciasxEquipo(df_shots, selected_team_rel, True)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats['accs_by_hex'] = rel_hexbin_stats[0] - base_hexbin_stats[0]

    fig = go.Figure()

    court = draw_plotly_fiba_court(fig)

    add_traces_to_court(court, rel_hexbin_stats)

    # DEFENSIVA
    # Crea hexagonos para el equipo seleccionado y calcula las estadisticas para esos hexagonos

    rel_hexbin_stats_def = calcular_Hexagonos_y_frecuenciasxEquipo(df_shots, selected_team_rel, False)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats_def['accs_by_hex'] = rel_hexbin_stats_def[0] - base_hexbin_stats[0]

    fig2 = go.Figure()
    court2 = draw_plotly_fiba_court(fig2)
    add_traces_to_court(court2, rel_hexbin_stats_def)

    # SCATTER PLOT DE ASISTENCIAS
    pointsperplayer_team = pointsperplayer[pointsperplayer['team_name']==selected_team_rel]

    fig3 = go.Figure(data=go.Scatter(
        x=pointsperplayer_team['assisted'],
        y=pointsperplayer_team['not_assisted'],
        mode='markers',
        hovertemplate=
        '<b>%{text}</b>' +
        '<br><i>assisted</i>: %{x}' +
        '<br><i>not_assisted</i>: %{y}',
        text=pointsperplayer_team['player_x'],
        marker=dict(
            size=10,  # set color equal to a variable
            colorscale='YlGnBu',  # one of plotly colorscales
            showscale=False
        )
    ))

    fig3.update_xaxes(showspikes=True)
    fig3.update_yaxes(showspikes=True)

    fig3.update_layout(
        title="Plot Title",
        xaxis_title="Points Assisted",
        yaxis_title="Points NOT Assisted")

    # PARCAT PLOT DE ASISTENCIAS


    playbyplay_assisted = playbyplay_points[
        (playbyplay_points['Complementary_player'].notnull()) & (playbyplay_points['team_name'] == selected_team_rel)]
    pbp_parcat_assisted = playbyplay_assisted.groupby(['player_x', 'Complementary_player'])['points'].sum()
    pbp_parcat_assisted = pd.DataFrame(pbp_parcat_assisted)
    pbp_parcat_assisted.reset_index(inplace=True)
    pbp_parcat_assisted.sort_values('points', ascending=False)

    fig4 = go.Figure(go.Parcats(
        dimensions=[
            {'label': 'Asistidor',
             'values': pbp_parcat_assisted['Complementary_player']},
            {'label': 'Anotador',
             'values': pbp_parcat_assisted['player_x']}],
        counts=pbp_parcat_assisted['points'],
        line={'color': pbp_parcat_assisted['points'], 'colorscale': 'YlGnBu'}
    ))

    # SUNBURST PLOT DE ASISTENCIAS
    pbp_sunburst_points = playbyplay_points[playbyplay_points['team_name'] == selected_team_rel]
    pbp_sunburst_points = pd.DataFrame(
        pbp_sunburst_points.groupby(['player_x', 'Complementary_player'])['points'].sum())
    pbp_sunburst_points.reset_index(inplace=True)
    pbp_sunburst_points['Assist'] = pbp_sunburst_points['Complementary_player'].apply(
        lambda x: 'NOT Assisted' if x is None else 'Assisted')
    fig5 = px.sunburst(pbp_sunburst_points, path=['player_x', 'Assist', 'Complementary_player'], values='points')

    return court, court2, fig3, fig4, fig5

#EQUIPO RIVAL
@app.callback(
    [Output('graph-court-def-rival', 'figure'), Output('graph-court-off-rival', 'figure')],
    [Input('dropdown-team-rival', 'value')])
def update_figure(selected_team_rel):
    # OFENSIVA
    # Crea hexagonos para el equipo seleccionado y calcula las estadisticas para esos hexagonos

    rel_hexbin_stats = calcular_Hexagonos_y_frecuenciasxEquipo(df_shots, selected_team_rel, False)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats['accs_by_hex'] = rel_hexbin_stats[0] - base_hexbin_stats[0]

    fig = go.Figure()

    court = draw_plotly_fiba_court(fig)

    add_traces_to_court(court, rel_hexbin_stats)

    # DEFENSIVA
    # Crea hexagonos para el equipo seleccionado y calcula las estadisticas para esos hexagonos

    rel_hexbin_stats_def = calcular_Hexagonos_y_frecuenciasxEquipo(df_shots, selected_team_rel, True)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats_def['accs_by_hex'] = rel_hexbin_stats_def[0] - base_hexbin_stats[0]

    fig2 = go.Figure()
    court2 = draw_plotly_fiba_court(fig2)
    add_traces_to_court(court2, rel_hexbin_stats_def)

    return court, court2

#Actualiza el dropdown de los jugadores de acuerdo al equipo seleccionado
@app.callback(
    Output('dropdown-player-local', 'options'),
    [Input('dropdown-team-local', 'value')]
)
def update_dropdown_player_local(team):
    return [{'label': i, 'value': i} for i in all_team_players[team]]

# @app.callback(
#     Output('dropdown-player-rival', 'options'),
#     [Input('dropdown-team-rival', 'value')]
# )
# def update_dropdown_player_local(team):
#     return [{'label': i, 'value': i} for i in all_team_players[team]]

#Actualizar tiros del jugador
@app.callback(
    [Output('graph-court-local-player', 'figure'), Output('graph-court-local-player_in_field', 'figure'),
     Output('court_team_shots_player_not_in_field', 'figure'), Output('court_team_defense_player_in_field', 'figure'),
     Output('court_team_defense_player_not_in_field', 'figure')],
    [Input('dropdown-player-local', 'value'),Input('dropdown-team-local', 'value')]
)
def update_figure(player, selected_team_rel):

    #CALCULA TIROS DEL JUGADOR
    rel_hexbin_stats_player = calcular_Hexagonos_y_frecuenciaxJugador_Tirador(df_shots, player)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats_player['accs_by_hex'] = rel_hexbin_stats_player[0] - base_hexbin_stats[0]

    fig = go.Figure()

    court_player_shots = draw_plotly_fiba_court(fig)

    add_traces_to_court(court_player_shots, rel_hexbin_stats_player)

    #CALCULA LOS TIROS DEL EQUIPO CON EL JUGADOR EN CANCHA (SIN CONTAR TIROS DEL JUGADOR)
    df_shots1 = deepcopy(df_shots)
    df_shots_without_player = df_shots1[df_shots1['player_x'] != player]
    rel_hexbin_stats_player_in_field = pbp_player_in_field(df_shots_without_player, selected_team_rel, player)
    rel_hexbin_stats_player_in_field = calcular_Hexagonos_y_frecuenciasxEquipo(rel_hexbin_stats_player_in_field, selected_team_rel, True)
    rel_hexbin_stats_player_in_field['accs_by_hex'] = rel_hexbin_stats_player_in_field[0] - base_hexbin_stats[0]

    fig_team_shots_player_in_field = go.Figure()

    court_team_shots_player_in_field = draw_plotly_fiba_court(fig_team_shots_player_in_field)

    add_traces_to_court(court_team_shots_player_in_field, rel_hexbin_stats_player_in_field)

    # CALCULA LOS TIROS DEL EQUIPO SIN EL JUGADOR EN CANCHA (SIN CONTAR TIROS DEL JUGADOR
    rel_hexbin_stats_player_not_in_field = pbp_player_not_in_field(df_shots_without_player, selected_team_rel, player)
    print(df_shots_without_player.columns)
    rel_hexbin_stats_player_not_in_field = calcular_Hexagonos_y_frecuenciasxEquipo(rel_hexbin_stats_player_not_in_field, selected_team_rel, True)
    rel_hexbin_stats_player_not_in_field['accs_by_hex'] = rel_hexbin_stats_player_not_in_field[0] - base_hexbin_stats[0]

    fig_team_shots_player_not_in_field = go.Figure()

    court_team_shots_player_not_in_field = draw_plotly_fiba_court(fig_team_shots_player_not_in_field)

    add_traces_to_court(court_team_shots_player_not_in_field, rel_hexbin_stats_player_not_in_field)

    #CALCULA LA DEFENSA DEL EQUIPO CON EL JUGADOR EN CANCHA

    rel_hexbin_stats_defense_player_in_field = pbp_player_in_field(df_shots1, selected_team_rel, player)
    rel_hexbin_stats_defense_player_in_field = calcular_Hexagonos_y_frecuenciasxEquipo(rel_hexbin_stats_defense_player_in_field,
                                                                               selected_team_rel, False)

    rel_hexbin_stats_defense_player_in_field['accs_by_hex'] = rel_hexbin_stats_defense_player_in_field[0] - base_hexbin_stats[0]

    fig_team_defense_player_in_field = go.Figure()

    court_team_defense_player_in_field = draw_plotly_fiba_court(fig_team_defense_player_in_field)

    add_traces_to_court(court_team_defense_player_in_field, rel_hexbin_stats_defense_player_in_field)

    # CALCULA LA DEFENSA DEL EQUIPO SIN EL JUGADOR EN CANCHA

    rel_hexbin_stats_defense_player_not_in_field = pbp_player_not_in_field(df_shots1, selected_team_rel, player)
    rel_hexbin_stats_defense_player_not_in_field = calcular_Hexagonos_y_frecuenciasxEquipo(rel_hexbin_stats_defense_player_not_in_field,
                                                                               selected_team_rel, False)

    rel_hexbin_stats_defense_player_not_in_field['accs_by_hex'] = rel_hexbin_stats_defense_player_not_in_field[0] - base_hexbin_stats[0]

    fig_team_defense_player_not_in_field = go.Figure()

    court_team_defense_player_not_in_field = draw_plotly_fiba_court(fig_team_defense_player_not_in_field)

    add_traces_to_court(court_team_defense_player_not_in_field, rel_hexbin_stats_defense_player_not_in_field)

    return court_player_shots, court_team_shots_player_in_field, court_team_shots_player_not_in_field, court_team_defense_player_in_field, court_team_defense_player_not_in_field


# # Comienzo Monitoreo
# starttime = timeit.default_timer()
# print("The start time is :", starttime)
# # Fin monitoreo tiempo
# print("The time difference is :", timeit.default_timer() - starttime)


if __name__ == '__main__':  
    app.run_server(debug=True, port=8050)
