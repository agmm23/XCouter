# IMPORTS
import sqlalchemy as db
#import mysql.connector
#from datetime import datetime

import pandas as pd
#from funciones import *
from funciones_panda import *

desired_width = 320
desired_columns = 30
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Get the df with playbyplay ordered by match_id and actionNumber

fields = "Clave, id_match, gt, team_name, team_rival, player_x AS player , actionNumber, actionType_x actionType,  subType_x as subType , previousAction_x , " \
         "`lead`,  s1, s2, scoring,  success, tno_x AS tno,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;" #traigo df sin team vacío ordenado por match y actionNumber

#pbp of all the matches in the DB
pbp = pbp(query)

#Agregar a la columna assistant quien fue el jugador que asistió en ese punto
#Toma una fila con anotacion y evalua la fila anterior si es que tuvo una asistencia, y agrega el jugador a la colunmna assistant

pbp['assistant'] = pbp['player'].shift().where( (pbp['tno'].shift() == pbp['tno'])
                                                          & (pbp['actionType'].isin(['2pt','3pt','freethrow']))
                                                             & (pbp['actionType'].shift() == 'assist')
                                                             )





#pbp of selected match_ids
#match_ids = ['1381246', '1541195', '1381247']
#df_team = match_pbp(df, match_ids)
#stats = stats_df(df_team)

match_ids = ['1381241']  # https://www.fibalivestats.com/u/FUBB/1381241/index_en_AU.html
df_team = match_pbp(pbp, match_ids)

stats = stats_df(df_team)
print(stats)

