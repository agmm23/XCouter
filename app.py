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
import timeit

# region Variables Declaration

Court_width = 1500
Court_height = 1400
threept_break_y = 300
three_area = 675


# endregion


#  Cancha FIBA - Funcion para dibujar cancha
# Cancha FIBA
def draw_plotly_fiba_court(fig, fig_width=600, margins=10):
    import numpy as np

    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200,
                    closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (Court_height + 2 * margins) / (Court_width + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[0 - margins, Court_width + margins])
    fig.update_yaxes(range=[0 - margins, Court_height + margins])

    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=0, y0=0, x1=Court_width, y1=Court_height,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=(Court_width - 490) / 2, y0=0, x1=(Court_width - 490) / 2 + 490, y1=580,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            # dict(
            # type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
            # line=dict(color=main_line_col, width=1),
            # fillcolor='#333333',
            # layer='below'
            # ),
            dict(
                type="circle", x0=(Court_width - 360) / 2, y0=(580 - 360 / 2), x1=(Court_width - 360) / 2 + 360,
                y1=(580 + 360 / 2), xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer='below'
            ),
            # dict(
            # type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
            # line=dict(color=main_line_col, width=1),
            # layer='below'
            # ),

            # Aro
            dict(
                type="rect", x0=(Court_width - 10) / 2, y0=120, x1=(Court_width - 10) / 2 + 10, y1=120 + 15,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=(Court_width - 45) / 2, y0=(120 + 15), x1=(Court_width - 45) / 2 + 45,
                y1=(120 + 15 + 45), xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=(Court_width - 180) / 2, y0=120, x1=(Court_width - 180) / 2 + 180, y1=120,
                line=dict(color="#ec7607", width=1),
            ),

            # Ejemplo de ares imaginarias
            # dict(type="path",
            # path=ellipse_arc(x_center=Court_width/2, y_center=(120+15+45/2), a=675/4, b=675/4, start_angle=0, end_angle=np.pi/2),
            # line=dict(color=main_line_col, width=1), layer='below',  fillcolor="blue", opacity=0.3),
            # dict(type="path",
            # path=ellipse_arc(x_center=Court_width/2, y_center=(120+15+45/2), a=675/4*2, b=675/4*2, start_angle=0, end_angle=np.pi*2),
            # line=dict(color=main_line_col, width=1), layer='below',  fillcolor="gray", opacity=0.3),
            # dict(type="path",
            # path=ellipse_arc(x_center=Court_width/2, y_center=(120+15+45/2), a=675/4*3, b=675/4*3, start_angle=0, end_angle=np.pi*2),
            # line=dict(color=main_line_col, width=1), layer='below',  fillcolor="gray", opacity=0.3),

            # Arco de 3
            dict(type="path",
                 path=ellipse_arc(x_center=Court_width / 2, y_center=(120 + 15 + 45 / 2), a=125, b=125, start_angle=0,
                                  end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(x_center=Court_width / 2, y_center=(120 + 15 + 45 / 2), a=675, b=675,
                                  start_angle=0.21, end_angle=np.pi - 0.21),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=90, y0=0, x1=90, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=Court_width - 90, y0=0, x1=Court_width - 90, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            # dict(
            # type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
            # line=dict(color=three_line_col, width=1), layer='below'
            # ),

            # dict(
            # type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=250, y0=227.5, x1=220, y1=227.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=90, y0=17.5, x1=80, y1=17.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=90, y0=27.5, x1=80, y1=27.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=90, y0=57.5, x1=80, y1=57.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),
            # dict(
            # type="line", x0=90, y0=87.5, x1=80, y1=87.5,
            # line=dict(color=main_line_col, width=1), layer='below'
            # ),

            # dict(type="path",
            # path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
            # line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return fig


# Funcion que convierte las coordenadas obtenidas a las coordenadas del dash court
def transform_coordinates(x_pos, y_pos, result, x_adjust=0, y_adjust=0, x_reference='left', y_reference='top'):
    # Es necesario invertir las coordenadas ya que la cancha esta al reves
    court_width = 1500
    court_height = 1400

    # x_pos se multiplica por dos ya que en el original toma toda la cancha, pero aca solamente la mitad

    if x_pos < 50:
        y_court = (x_pos * 2 + y_adjust) * court_height / 100
        if y_reference == 'top':
            x_court = (y_pos + x_adjust) * court_width / 100
        else:
            x_court = (100 - y_pos + x_adjust) * court_width / 100
    else:
        y_court = ((100 - x_pos) * 2 + y_adjust) * court_height / 100
        if y_reference == 'top':
            x_court = (100 - y_pos + x_adjust) * court_width / 100
        else:
            x_court = (y_pos + x_adjust) * court_width / 100

    return (x_court, y_court)


# Funcion distancia al aro
def distancia_aro(x, y):
    shot = np.array((x, y))
    x_aro = 1500 / 2
    y_aro = 120 + 15 + 45 / 2
    aro = np.array((x_aro, y_aro))

    return np.linalg.norm(shot - aro)


# Funcion que genera hexagonos a partir de un dataframe
def create_hexagons(df_shots):
    plt.figure(figsize=(0.05, 0.05))
    # plt.axis('off')
    # HB = plt.hexbin(x, y, gridsize=25, cmap=cmocean.cm.algae , mincnt=1) # cmocean.cm.algae is a cmocean colormap

    df_success_shots = df_shots[df_shots['success'] == 1]
    df_missed_shots = df_shots[df_shots['success'] == 0]

    plt.axis('off')

    gridsize = 50

    # Genera un hexagono/bin con un conjunto de coordenadas

    # Para el total de los tiros
    HB_total_shots = plt.hexbin(df_shots['x_converted'], df_shots['y_converted'],  # , mincnt=1, C=df_shots['success'],
                                gridsize=gridsize, extent=(0, 1500, 0, 1400))
    # Para los tiros exitosos
    HB_success_shots = plt.hexbin(df_success_shots['x_converted'], df_success_shots['y_converted'],
                                  # extent=(0, 1500, 0, 1400), mincnt=1, C=df_shots['success'],
                                  gridsize=gridsize, extent=(0, 1500, 0, 1400))
    # Para los tiros errados
    HB_missed_shots = plt.hexbin(df_missed_shots['x_converted'], df_missed_shots['y_converted'],
                                 # extent=(0, 1500, 0, 1400), mincnt=1, C=df_shots['success'],
                                 gridsize=gridsize, extent=(0, 1500, 0, 1400))

    # Obtiene las coordenadas del centro del hexagono de todos los tiros
    x_HB = HB_total_shots.get_offsets()[:, 0]
    y_HB = HB_total_shots.get_offsets()[:, 1]

    # Obtiene la frecuencia, o sea la cantidad de ocurrencias computadas por el hexagono

    # Para el total de los tiros
    freq_by_hex = HB_total_shots.get_array()

    # Para los tiros exitosos y errados
    freq_by_hex_success_shots = HB_success_shots.get_array()
    freq_by_hex_missed_shots = HB_missed_shots.get_array()

    # Calcula el porcentaje de acierto y errores por hexagono  y convierte valores NaN en 0
    pcts_by_hex_success = freq_by_hex_success_shots / freq_by_hex
    pcts_by_hex_success[np.isnan(pcts_by_hex_success)] = 0  # convert NAN values to 0

    pcts_by_hex_missed = freq_by_hex_missed_shots / freq_by_hex
    pcts_by_hex_missed[np.isnan(pcts_by_hex_missed)] = 0  # convert NAN values to 0

    hexbin_stats = pd.DataFrame(
        {'x': x_HB, 'y': y_HB, 'freq_by_hex': freq_by_hex, 'freq_by_hex_success': freq_by_hex_success_shots,
         'freq_by_hex_missed_shots': freq_by_hex_missed_shots, 'pcts_by_hex_success': pcts_by_hex_success,
         'pcts_by_hex_missed': pcts_by_hex_missed})


    return hexbin_stats


# Funcion que calcula en que area es el tiro
def define_section(x, y, shot_distance, d1=125, d2=245, d3=491, d5=858):
    # Three points
    if x < 90 and y < threept_break_y:  # Three points
        section = 'three_corner_left'
    elif x > (Court_width - 90) and y < threept_break_y:
        section = "three_corner_right"
    elif d5 > shot_distance > three_area:
        if (Court_width - 490) / 2 + 490 <= x and y >= threept_break_y:
            section = 'short_three_right'
        elif (Court_width - 490) / 2 <= x <= (Court_width - 490) / 2 + 490:
            section = 'short_three_center'
        elif x < (Court_width - 90) and y >= threept_break_y:
            section = 'short_three_left'
        else:
            section = "NA"
    elif d5 <= shot_distance:
        if (Court_width - 490) / 2 > x:
            section = 'long_three_left'
        elif (Court_width - 490) / 2 <= x <= (Court_width - 490) / 2 + 490:
            section = 'long_three_center'
        elif (Court_width - 490) / 2 + 490 < x:
            section = 'long_three_right'
        else:
            section = "NA"
    # Two points
    elif shot_distance < d1:
        section = "ss_two"
    elif d1 <= shot_distance < d2:
        section = "short_two"
    elif d2 <= shot_distance < d3:
        if x < (Court_width - 490) / 2:
            if y < threept_break_y:
                section = "long_two_corner_left"
            else:
                section = "long_two_mid_left"
        elif (Court_width - 490) / 2 <= x <= (Court_width - 490) / 2 + 490:
            section = "long_two_center"
        elif x > (Court_width - 490) / 2 + 490:
            if y < threept_break_y:
                section = "long_two_corner_right"
            else:
                section = "long_two_mid_right"
        else:
            section = "NA"
    elif d3 <= shot_distance:
        if x < (Court_width - 490) / 2:
            if y < threept_break_y:
                section = "ll_two_corner_left"
            else:
                section = "ll_two_mid_left"
        elif (Court_width - 490) / 2 <= x <= (Court_width - 490) / 2 + 490:
            section = "ll_two_center"
        elif x > (Court_width - 490) / 2 + 490:
            if y < threept_break_y:
                section = "ll_two_corner_right"
            else:
                section = "ll_two_mid_right"
        else:
            section = "NA"
    else:
        section = "NA"

    return section


# Funcion que calcula el porcentaje de exitos por area de tiro
def calculate_succes_per_section(df):
    eff_x_section = df.groupby('shot_section')['freq_by_hex_success'].sum() / df.groupby('shot_section')[
        'freq_by_hex'].sum()

    eff_x_section = pd.DataFrame(eff_x_section)

    eff_x_section.reset_index(inplace=True)

    df = pd.merge(df, eff_x_section, on='shot_section')
    return df


# Funcion que calcula el porcentaje asociado a la frecuencia de cada hexagono
def calculate_freq_x_hex(df):
    total_shots = df['freq_by_hex'].sum()
    df['frequency'] = df['freq_by_hex'].apply(lambda x: x / total_shots)
    return df


# Funcion que agrega los hexagonos a la cancha se le pasa la figura y un df con los calculos, incluye una columna que
# compara la diferencia con la linea base
def add_traces_to_court(court, rel_hexbin_stats):
    colorscale = 'RdYlBu_r'
    marker_cmin = -0.05
    marker_cmax = 0.05
    opacity = 0.75

    max_freq = 0.002
    freq_by_hex = np.array([min(max_freq, i) for i in rel_hexbin_stats['frequency']])

    ticktexts = [str(marker_cmin * 100) + '%-', "", str(marker_cmax * 100) + '%+']
    accs_by_hex_text = rel_hexbin_stats['accs_by_hex']
    freq_by_hex_text = rel_hexbin_stats['frequency']

    hexbin_text = [
        '<i>Accuracy: </i>' + str(round(accs_by_hex_text[i] * 100, 1)) + '%<BR>'
                                                                         '<i>Frequency: </i>' + str(
            round(freq_by_hex_text[i] * 100, 2)) + '%'
        for i in range(len(freq_by_hex_text))
    ]

    court.add_trace(go.Scatter(x=rel_hexbin_stats['x'], y=rel_hexbin_stats['y'],
                               mode='markers',
                               marker=dict(
                                   size=freq_by_hex, sizemode='area', sizeref=2. * max(freq_by_hex) / (11. ** 2),
                                   sizemin=2.5,
                                   color=rel_hexbin_stats['accs_by_hex'], colorscale=colorscale,
                                   colorbar=dict(
                                       thickness=15,
                                       x=0.84,
                                       y=0.87,
                                       yanchor='middle',
                                       len=0.2,
                                       title=dict(
                                           text="<B>Efectividad</B>",
                                           font=dict(
                                               size=11,
                                               color='#4d4d4d'
                                           )

                                       ),
                                       tickvals=[marker_cmin, (marker_cmin + marker_cmax) / 2, marker_cmax],
                                       ticktext=ticktexts,
                                       tickfont=dict(
                                           size=11,
                                           color='#4d4d4d'
                                       ),
                                   ), cmin=marker_cmin, cmax=marker_cmax,
                                   line=dict(width=1, color='#333333'), symbol='hexagon', opacity=opacity
                               ),
                               text=hexbin_text,
                               hoverinfo='text'
                               ))

def recibir_df_y_calcular_hexagonos(df):
    hex_stats = create_hexagons(df)
    hex_stats['distance'] = hex_stats.apply(lambda a: distancia_aro(a['x'], a['y']), axis=1)
    hex_stats['shot_section'] = hex_stats.apply(lambda a: define_section(a['x'], a['y'], a['distance']),
                                                          axis=1)

    # Calcula estadisticas comparativas para el equipo
    hex_stats = calculate_succes_per_section(hex_stats)
    hex_stats = calculate_freq_x_hex(hex_stats)
    return hex_stats


def calcular_Hexagonos_y_frecuenciasxEquipo(df_shots, team,ofensiva):
    if ofensiva:
        df_shots_team = df_shots[df_shots.team_name == team]
    else:
        df_shots_team = df_shots[df_shots.team_rival == team]

    hex_stats_team = recibir_df_y_calcular_hexagonos(df_shots_team)
    return hex_stats_team

def calcular_Hexagonos_y_frecuenciaxJugador_Tirador(df_shots, player):
    df_shots_player = df_shots[df_shots.player_x == player]
    hex_stats_player = recibir_df_y_calcular_hexagonos(df_shots_player)
    return hex_stats_player

    filtered_df = df[df.player_x == selected_player_a]
# # Importar a un dataframe los datos para realizar pruebas
# connect_string = 'mysql+mysqlconnector://root:password@localhost:3306/scouter'
# sql_engine = sql.create_engine(connect_string)
# pbp_query = "select * from playbyplay"
# df = pd.read_sql_query(pbp_query, sql_engine)
#
# df['temporary'] = df.apply (lambda a: transform_coordinates(a['x'],a['y'],0,0,0,'left','bottom'), axis=1)
# df['x_converted'] = df['temporary'].apply (lambda x: x[0])
# df['y_converted'] = df['temporary'].apply (lambda x: x[1])
# df.drop('temporary', axis=1, inplace = True)

# region Conectar a base de datos y traer a un dataframe
def table(query):
    import pandas as pd
    results = connection.execute(query).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    return df

connect_string = 'mysql+mysqlconnector://root:monic.123@localhost:3306/scouter'
engine = sql.create_engine(connect_string, connect_args={'auth_plugin': 'mysql_native_password'})
connection = engine.connect()

query = "select * from playbyplay;"
metadata = sql.MetaData()

playbyplay = sql.Table('playbyplay', metadata, autoload=True, autoload_with=engine)
query = "select * from playbyplay;"
df = table(query)


##connect_string = 'mysql+mysqlconnector://root:passwordd@localhost:3306/scouter'

#sql_engine = sql.create_engine(connect_string)
#df = pd.read_sql_query(pbp_query, sql_engine)

df_shots = df[['id_match', 'actionType_x', 'player_x', 'success', 'team_name', 'team_rival', 'x', 'y']]
df_shots = df_shots[df_shots['actionType_x'].isin(['2pt', '3pt'])]
# endregion

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
        html.H2('Jugador Local'),
        dcc.Dropdown(
            id='dropdown-player-local',
            value='ALL'),
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H2('Jugador Rival'),
        dcc.Dropdown(
            id='dropdown-player-rival',
            value='ALL'),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Jugador Local'),
        dcc.Graph(id='graph-court-local-player')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        html.H1('Jugador Rival'),
        dcc.Graph(id='graph-court-rival-player')
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
]
)

#EQUIPO LOCAL
@app.callback(
    [Output('graph-court-off', 'figure'), Output('graph-court-def', 'figure')],  # todo agregar la figura defensiva
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

    return court, court2

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

#Actualiza el dropodown de los jugadores de acuerdo al equipo seleccionado
@app.callback(
    Output('dropdown-player-local', 'options'),
    [Input('dropdown-team-local', 'value')]
)
def update_dropdown_player_local(team):
    return [{'label': i, 'value': i} for i in all_team_players[team]]

@app.callback(
    Output('dropdown-player-rival', 'options'),
    [Input('dropdown-team-rival', 'value')]
)
def update_dropdown_player_local(team):
    return [{'label': i, 'value': i} for i in all_team_players[team]]

#Actualizar tiros del jugador
@app.callback(
    Output('graph-court-local-player', 'figure'),
    [Input('dropdown-player-local', 'value')]
)
def update_figure(player):
    rel_hexbin_stats = calcular_Hexagonos_y_frecuenciaxJugador_Tirador(df_shots, player)

    # Compara $ aciertos del equipo versus % aciertos de la liga
    rel_hexbin_stats['accs_by_hex'] = rel_hexbin_stats[0] - base_hexbin_stats[0]

    fig = go.Figure()

    court = draw_plotly_fiba_court(fig)

    add_traces_to_court(court, rel_hexbin_stats)

    return court


#Jugador Local #todo acomodar la funcion que carga hexagonos por equipo para que lo haga por jugadores tambien y a partir de ahi invocar al callback por jugador
# @app.callback(
#     Output('graph-court-local-player', 'figure'),
#     [Input('dropdown-player-local', 'value')])
# def update_figure(selected_player):

#     filtered_df = df[df.player_x == selected_player_a]
#     filtered_df_scored = filtered_df[filtered_df.success == 1]
#     filtered_df_missed = filtered_df[filtered_df.success == 0]
#     fig = go.Figure()
#     court = draw_plotly_fiba_court(fig)
#     court.add_trace(
#         go.Scatter(x=filtered_df_scored.x_converted, y=filtered_df_scored.y_converted, marker=dict(symbol='circle', size=15, color='green', opacity=1.0),
#                    mode='markers'))
#     court.add_trace(
#         go.Scatter(x=filtered_df_missed.x_converted, y=filtered_df_missed.y_converted, marker=dict(symbol='x', size=15, color='red', opacity=1.0),
#                mode='markers'))
#     return court




# # Comienzo Monitoreo
# starttime = timeit.default_timer()
# print("The start time is :", starttime)
# # Fin monitoreo tiempo
# print("The time difference is :", timeit.default_timer() - starttime)


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
