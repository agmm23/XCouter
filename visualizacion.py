# IMPORTS
import sqlalchemy as db
#import mysql.connector
from datetime import datetime

#import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

import pandas as pd
#from funciones import *
from funciones_panda import *

desired_width = 320
desired_columns = 25
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', desired_columns)
pd.set_option('display.max_rows', desired_rows)

# Conectar a la DB
connect_string = 'mysql+mysqlconnector://root:monic.123@localhost:3306/scouter'

#fields = "Clave, id_match, actionNumber, team_name, team_rival, actionType_x, gt,  `lead`, period,  player_x,  pno_x, previousAction_x, s1, s2, " \
#         "scoring,  subType_x, success, tno_x,  per, perType,  r, shirtNumber_y, subType_y, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x," \
#         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

fields = "Clave, id_match, gt, team_name, team_rival, player_x , actionNumber, actionType_x ,  subType_x  , previousAction_x , " \
         "`lead`,   s1, s2, scoring,  success, tno_x,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;" #traigo df sin team vacío ordenado por team y actionNumber

engine = db.create_engine(connect_string, connect_args={'auth_plugin': 'mysql_native_password'})
connection = engine.connect()

df = table(query, connection)  # PBP

#print(df)


#match_ids = MATCHES (df, 'HEBRAICA Y MACABI')
match_ids = ALL_MATCHES (df)

#match_ids = ['1381246', '1541195', '1381247']
#match_ids = ['1381246', '1381247']

df_team = match_pbp(df, match_ids)    #.sort_values(['id_match', 'actionNumber'], ascending=[True, False])

#ravel

#start = datetime.now()

stats = STATS(df_team)   #.loc[ 'HEBRAICA Y MACABI' , : ]
print(stats)
breakpoint()
stats.reset_index(inplace=True)
#print(stats)
x = stats[stats["TEAM"] == "HEBRAICA Y MACABI"]
print(x)

data = [go.Scatterpolar(
  r = [x['DR%'].values[0],x['OR%'].values[0],x['TOV%'].values[0],x['eFG%'].values[0],x["FTR"].values[0]],
  theta = ['DR%','OR%','TOV%','eFG%','FTR'],
  fill = 'toself',
     line =  dict(
            color = 'yellow'
        )
)]

layout = go.Layout(
  polar = dict(
    radialaxis = dict(
      visible = True,
      range = [0, 1]
    )
  ),
  showlegend = False,
  title = "{} stats distribution".format(x.TEAM.values[0])
)
fig = go.Figure(data=data, layout=layout)

iplot(fig, filename = "ESTADISTICAS")


