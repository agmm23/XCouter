# IMPORTS
import sqlalchemy as db
#import mysql.connector
#from datetime import datetime
from openpyxl import load_workbook
import xlsxwriter

import pandas as pd
#from funciones import *
from match_functions import *
from team_stats import *
from possessions import *

from openpyxl import load_workbook


desired_width = 320
desired_columns = 30
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Get the df with playbyplay ordered by match_id and actionNumber

fields = "Clave, id_match, gt, team_name, team_rival, player_x AS player , actionNumber, actionType_x AS actionType,  subType_x AS subType , previousAction_x AS previousAction, " \
         "`lead`,  s1, s2, scoring,  success, tno_x AS tno,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
         "Player_1_Local, Player_2_Local, Player_3_Local, Player_4_Local, Player_5_Local, Player_1_Visitor, Player_2_Visitor, Player_3_Visitor, Player_4_Visitor, Player_5_Visitor, x, y"

#traigo df sin team vacío ordenado por match y actionNumber - para stats
#query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;"

query = "select " + fields + " from playbyplay order by id_match, actionNumber ASC;"
#pbp of all the matches in the DB
#pbp = pbp(query)

#Agregar a la columna assistant quien fue el jugador que asistió en ese punto
#Toma una fila con anotacion y evalua la fila anterior si es que tuvo una asistencia, y agrega el jugador a la colunmna assistant

#pbp['assistant'] = pbp['player'].shift().where( (pbp['tno'].shift() == pbp['tno'])
#                                                          & (pbp['actionType'].isin(['2pt','3pt','freethrow']))
#                                                             & (pbp['actionType'].shift() == 'assist')
#                                                             )


#pbp of selected match_ids
#match_ids = ['1381246', '1541195', '1381247']
#df_team = match_pbp_df(pbp, match_ids)
#stats = stats_df(df_team)


#match_ids = ['1381241']  # https://www.fibalivestats.com/u/FUBB/1381241/index_en_AU.html
#df_team = match_pbp(pbp, match_ids)

#stats = stats_df(df_team)
#print(stats)
#print(stats[['FG','FGA','2PT', '2PTA','3PT', '3PTA','FT','FTA', 'AST', 'STL', 'BLK', 'TO']])

#Possessions:
#df: pbp of all the matches in the DB
pbp = pbp(query)
#match_id = ['1486001']
#query = "select " + fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;"
#pbp = pbp(query)
#match_pbp = match_pbp_df(pbp, match_id)
#visualize_possessions(match_pbp, match_id)


#match_ids = pbp['id_match'].unique()  # num


match_ids = ['1381246', '1541195', '1381247', '1486001']
match_ids = ['1381246']
path = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/"

match_pbp = match_pbp_df(pbp, match_ids)
#possessions = team_possessions(match_pbp, match_ids)
#possessions2 = match_possessionsv2(match_pbp, match_ids)
#pbp = pbp_possessions_df(match_pbp, match_ids)
#print(pbp)

#print(possessions2.equals(possessions))
#file =  match_ids[0] + 'org.xlsx'
#possessions.to_excel(path + file, sheet_name=match_ids[0], engine='xlsxwriter')
#file =  match_ids[0]  + 'new.xlsx'
#pbp.to_excel(path + file, sheet_name=match_ids[0], engine='xlsxwriter')

#path = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/"
#match_ids = ['1486001']
#
match_ids = all_matches(pbp)
#match_ids = ['1486001']
##Generar los archivos de posesiones para todos los partidos de la base
for i in match_ids:
    file = i + '.xlsx'
    match_pbp = pbp_possessions_df(pbp, [i])
#    possessionsChange = visualize_possessions(match_pbp, [i])
#    print(match_pbp)
    match_pbp.to_excel(path + file, sheet_name=match_ids[0], engine='xlsxwriter')
#    possessions = team_possessions(match_pbp, [i])
#    print(possessions)
##    with pd.ExcelWriter(path + file, engine='openpyxl', mode='a') as writer:
##        pos[['team_name', 'pos_no', 'pos_sec']].to_excel(writer, sheet_name='possessions')
#
#
#'''
#1486001
#print(possessions(match_pbp, match_id))


#    pbp = pbp(query)
#    match_pbp = match_pbp_df(pbp, match_ids)

#https://stackoverflow.com/questions/62419264/update-multiple-rows-in-mysql-with-pandas-dataframe/62422786#62422786
