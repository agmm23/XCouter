# IMPORTS
import sqlalchemy as db
#import mysql.connector
#from datetime import datetime

import pandas as pd
#from funciones import *
from funciones_panda import *

desired_width = 320
desired_columns = 25
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', desired_columns)
pd.set_option('display.max_rows', desired_rows)

# Get the df with playbyplay ordered by match_id and actionNumber

fields = "Clave, id_match, gt, team_name, team_rival, player_x , actionNumber, actionType_x ,  subType_x  , previousAction_x , " \
         "`lead`,  s1, s2, scoring,  success, tno_x,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;" #traigo df sin team vacío ordenado por match y actionNumber

#pbp of all the matches in the DB
df = pbp(query)



#pbp of selected match_ids
#match_ids = ['1381246', '1541195', '1381247']
#df_team = match_pbp(df, match_ids)
#stats = stats_df(df_team)

stats = stats_df(df)
print(stats)
