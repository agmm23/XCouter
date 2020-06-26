# IMPORTS
import sqlalchemy as db
#import mysql.connector
#from datetime import datetime

import pandas as pd
#from funciones import *
from team_stats import *

desired_width = 320
desired_columns = 25
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', desired_columns)
pd.set_option('display.max_rows', desired_rows)

# Get the df with playbyplay ordered by match_id and actionNumber

fields = "Clave, id_match, gt, team_name, team_rival, player_x AS player , actionNumber, actionType_x actionType,  subType_x AS subType , previousAction_x , " \
         "`lead`,  s1, s2, scoring,  success, tno_x AS tno,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;" #traigo df sin team vacío ordenado por match y actionNumber

#df: pbp of all the matches in the DB
pbp = pbp(query)

#print(df)


#match_ids = all_matches(df) # no aporta
''''
match_ids = [1381246] #agu-say
#match_ids = ['1381246', '1541195', '1381247']
#match_ids = ['1381246', '1381247']

#df_team = match_pbp(df, match_ids)    # where df = pbp(query)

#ravel


stats = stats_df(pbp)
#stats = stats_df(df_team)  #
print(stats)

print(orb(stats, 'AGUADA'))
print(drb(stats, 'AGUADA'))

print(orb(stats, 'SAYAGO'))
print(drb(stats, 'SAYAGO'))



print(drebp(stats, 'AGUADA')) #0.719745
print(orebp(stats, 'ATENAS')) #0.267974
print(ftrate(stats, 'URUNDAY UNIVERSITARIO')) #0.326475


#print(drp(stats, 'AGUADA'))
#print(orp(stats, 'SAYAGO'))
#print(drp(stats, 'SAYAGO'))


df_team = stats

print('AGUADA ORB', orb(df_team, 'AGUADA'))  #0
print('AGUADA DRB', drb(df_team, 'AGUADA'))  #1
print('AGUADA OppORB', opp_orb(df_team, 'AGUADA'))  #4
print('OppDRB AGUADA', opp_drb(df_team, "AGUADA")) #3
print('AGUADA ORB%', orebp(df_team, 'AGUADA'))
print('AGUADA DRB%', drebp(df_team, 'AGUADA'))

print('D SPORTING ORB', orb(df_team, 'D SPORTING'))  #9
print('D SPORTING DRB', drb(df_team, 'D SPORTING'))  #28
print('D SPORTING OppDRB', opp_drb(df_team, 'D SPORTING'))
print('D SPORTING OppORB', opp_orb(df_team, 'D SPORTING'))

print('URUNDAY ORB', orb(df_team, 'URUNDAY UNIVERSITARIO'))  #8
print('URUNDAY DRB', drb(df_team, 'URUNDAY UNIVERSITARIO'))  #24
print('URUNDAY OppDRB', opp_drb(df_team, 'URUNDAY UNIVERSITARIO'))
print('URUNDAY OppORB', opp_orb(df_team, 'URUNDAY UNIVERSITARIO'))

print('SAYAGO ORB', orb(df_team, 'SAYAGO'))  #
print('SAYAGO DRB', drb(df_team, 'SAYAGO'))  #
print('SAYAGO OppORB', opp_drb(df_team, 'SAYAGO'))  #0
print('SAYAGO OppDRB', opp_drb(df_team, 'SAYAGO'))  #1
print('SAYAGO ORP%', orebp(df_team, 'SAYAGO'))
print('SAYAGO DRP%', drebp(df_team, 'SAYAGO'))

'''
#''' Verificar salidas de los Opp
# '1381246', '1381247' AGUADA - SAYAGO / AGUADA - TROUVILLE 
# '1541195' URUNDAY - DEFENSOR
match_ids = ['1381246', '1381247', '1541195']
match_ids = ['1381246', '1381247', '1541195']




df_team = match_pbp(pbp, match_ids)


stats = stats_df(df_team)

#Comparar los cruzados (Opp) - AGUADA SUMA SAY y TROU
print(stats[['ORB', 'DRB', 'OppORB', 'OppDRB', 'FG', 'OppFG', '3PT', 'Opp3PT', 'FG', 'OppFG', 'TO', 'OppTO', 'FGA', 'OppFGA']])
