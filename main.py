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
from plus_minus import *
from openpyxl import load_workbook


desired_width = 320
desired_columns = 30
desired_rows = 15
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Get the df with playbyplay ordered by match_id and actionNumber

pbp_fields = "Clave, id_match, gt, team_name, team_rival, player_x AS player , actionNumber, actionType_x AS actionType,  subType_x AS subType , previousAction_x AS previousAction, " \
         "`lead`,  s1, s2, scoring,  success, tno_x AS tno,  period,  perType,  shirtNumber_y,  pno_x , p, r, internationalFamilyName,  internationalFirstName, scoreboardName, shirtNumber_x, " \
             "Player_1_Name_Home AS h1, Player_2_Name_Home AS h2, Player_3_Name_Home AS h3, Player_4_Name_Home AS h4, Player_5_Name_Home AS h5," \
             "Player_1_Name_Away AS a1, Player_2_Name_Away AS a2, Player_3_Name_Away AS a3, Player_4_Name_Away AS a4, Player_5_Name_Away AS a5," \
             "x, y"
# "Player_1_Local AS h1, Player_2_Local AS h2, Player_3_Local AS h3, Player_4_Local AS h4, Player_5_Local AS h5, " \
#    "Player_1_Visitor AS a1, Player_2_Visitor AS a2, Player_3_Visitor AS a3, Player_4_Visitor AS a4, Player_5_Visitor AS a5, " \


pbp_query = "select " + pbp_fields + " from playbyplay order by id_match, period, actionNumber ASC;"


players_field = "id, match_id, id_team, local, shirt_number, player_name, starter"
players_query = "select " + pbp_query + " from players_x_match order by match_id, actionNumber ASC;"



#pbp of all the matches in the DB
#pbp = scouter(pbp_query)

#Agregar a la columna assistant quien fue el jugador que asistió en ese punto
#Toma una fila con anotacion y evalua la fila anterior si es que tuvo una asistencia, y agrega el jugador a la colunmna assistant

#scouter['assistant'] = scouter['player'].shift().where( (scouter['tno'].shift() == scouter['tno'])
#                                                          & (scouter['actionType'].isin(['2pt','3pt','freethrow']))
#                                                             & (scouter['actionType'].shift() == 'assist')
#                                                             )


#scouter of selected match_ids
#match_ids = ['1381246', '1541195', '1381247']
#df_team = match_pbp_df(scouter, match_ids)
#stats = stats_df(df_team)

#pbp = scouter(pbp_query)
#match_ids = ['1485999']
#df_team = match_pbp_df(pbp, match_ids)
#stats = stats_df(df_team)

#print(stats)
#19+ 6 = 35 +10 = 45


#match_ids = ['1381241']  # https://www.fibalivestats.com/u/FUBB/1381241/index_en_AU.html
#df_team = match_pbp(scouter, match_ids)

#stats = stats_df(df_team)
#print(stats)
#print(stats[['FG','FGA','2PT', '2PTA','3PT', '3PTA','FT','FTA', 'AST', 'STL', 'BLK', 'TO']])

#Possessions:
#df: scouter of all the matches in the DB
#pbp = scouter(pbp_query)
#players = scouter(players_query)
#match_id = ['1486001']
#pbp_query = "select " + pbp_fields + " from playbyplay where team_name != '' order by id_match, actionNumber ASC;"
#scouter = scouter(pbp_query)
#match_pbp = match_pbp_df(scouter, match_id)
#visualize_possessions(match_pbp, match_id)


#match_ids = scouter['id_match'].unique()  # num


#match_ids = ['1381246', '1541195', '1381247', '1486001']
#match_ids = ['1486001']

#Obtengo df para el match_id
#match_pbp = match_pbp_df(scouter, match_ids)


##pbp_possessions = pbp_possessions_df(match_pbp)
##print(pbp_possessions)
#possessions = team_possessions_qty(match_pbp, match_ids)
#possessions2 = match_possessionsv2(match_pbp, match_ids)
#pbp_pos = pbp_possessions_df(match_pbp)
#print(pbp_pos)


#match_ids = all_matches(pbp)
#match_ids = ['1485999']

##Generar los archivos de posesiones para todos los partidos de la base
path = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/"
#match_ids = ['1485998', '1485999']

pbp = scouter(pbp_query)
match_ids = ['1381247', '1381246']   #AGUADA
#match_ids = ['1381246']
match_pbp = match_pbp_df(pbp, match_ids)
team = "AGUADA"
player = 'L. Garcia Morales'
#aguada_morales_pbp = player_pbp_df(match_pbp, team, player)

#pbp_possessions = pbp_possessions_df(aguada_morales_pbp)

file = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/AGUADA_LGM_1381246_1381247.xlsx"
#pbp_possessions.to_excel(file, sheet_name=match_ids[0], engine='xlsxwriter')


#match_pbp = match_pbp_df(pbp,match_ids)  ## tengo que quedarme con jugadores
###filtered = match_pbp.where(match_pbp == 'AGUADA').dropna()
##player_name = "LEANDRO"
##player_fname = "GARCIA MORALES"
#shirt = 11
#filtered = match_pbp.loc[match_pbp[['a1','a2','a3','a4','a5','h1','h2','h3','h4','h5']].isin([shirt]).any(axis=1)]



for i in match_ids:
    print(i)
    file = i + '_nuevo' + '.xlsx'
    #obtengo scouter del match
    match_pbp = match_pbp_df(pbp, [i])
    #obtengo df con el scouter con numero de posesion y duracion
    pbp_possessions = pbp_possessions_df(match_pbp)
    #pbp_possessions = match_possessions_end(match_pbp)
    #possessions = team_posssessions_df(match_pbp, 'TROUVILLE')
    pbp_possessions.to_excel(path + file, sheet_name=match_ids[0], engine='xlsxwriter')
    print(pbp_possessions)

'''
pbp = scouter(pbp_query)     #obtengo df con pbp de todos los partidos
#match_ids = all_matches(pbp)
#print(type(match_ids))
#match_pbp = match_possessions_end(pbp)
#print(match_pbp.head())

path = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/"
#
#teams = all_teams(pbp)
#print(teams)
#match_ids = all_matches(pbp)
#match_pbp = match_pbp_df(pbp,match_ids)
#possessions = team_possessions_qty(match_pbp, 'URUNDAY UNIVERSITARIO')



#for i in teams[0:len(teams)]:
#   possessions = team_possessions_qty(pbp, i)
#   print(i + ' ')
#   print( possessions )
#   with pd.ExcelWriter(path + 'possession.xlsx',
#                       mode='a') as writer:
#       possessions.to_excel(writer)


match_ids = ['1485999', '1381247']
match_pbp = match_pbp_df(pbp,match_ids)
possessions_qty = team_possessions_qty(match_pbp, 'AGUADA')
possessions_qty1 = team_possessions_qty(match_pbp, 'TROUVILLE')
possessions_qty2 = team_possessions_qty(match_pbp, 'D SPORTING')
possessions_qty3 = team_possessions_qty(match_pbp, 'URUNDAY UNIVERSITARIO')
print(match_ids, 'AGUADA', possessions_qty, 'TROUVILLE', possessions_qty1, 'D SPORTING', possessions_qty2)
#
#match_ids = ['1485999']
#match_pbp = match_pbp_df(pbp,match_ids)
#possessions_qty = team_possessions_qty(match_pbp, 'TROUVILLE')
#possessions_qty1 = team_possessions_qty(match_pbp, 'D SPORTING')
#print(match_ids, 'TROUVILLE', possessions_qty, 'D SPORTING', possessions_qty1)
#
#pbp = scouter(pbp_query)
#match_ids = ['1381247']
#match_pbp = match_pbp_df(pbp,match_ids)
#possessions_qty = team_possessions_qty(match_pbp, 'AGUADA')
#possessions_qty1 = team_possessions_qty(match_pbp, 'TROUVILLE')
#print(match_ids, 'AGUADA', possessions_qty, 'TROUVILLE', possessions_qty1)

#possessions_mean1 = team_possessions_mean(match_pbp, 'TROUVILLE')
#possessions_mean2 = team_possessions_mean(match_pbp, 'AGUADA')
#print( possessions_mean2)
#print(possessions_mean1, possessions_mean2)

#1485999 TROUVILLE 72 D SPORTING 72
#1541195 D SPORTING 74 URUNDAY UNIVERSITARIO 74
#1381247 AGUADA 78 15.064102564102564  TROUVILLE 77 15.831168831168831  / 2 partidos 15.590604026845638
# ['1485999', '1381247'] AGUADA 78 TROUVILLE 149


#print(match_pbp.tail())
#print(match_pbp.head())
#print(match_pbp.tail())
##desired_width = 320
#desired_columns = 30
#desired_rows = 15
#pd.set_option('display.width', desired_width)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', 20)

#path = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/"
#
##AGUADA, TROUVILLE   - 1381247
## AGUADA D SPORTING       1381274
#match_ids = ['1381247', '1381274']


#match_pbp = match_pbp_df(pbp,match_ids)  ## tengo que quedarme con jugadores
###filtered = match_pbp.where(match_pbp == 'AGUADA').dropna()
##player_name = "LEANDRO"
##player_fname = "GARCIA MORALES"
#shirt = 11
#filtered = match_pbp.loc[match_pbp[['a1','a2','a3','a4','a5','h1','h2','h3','h4','h5']].isin([shirt]).any(axis=1)]
#
###filtered = match_pbp.isin([player])
#pbp_possessions = pbp_possessions_df_camiseta(filtered)
#file = "AGUADA_LGM.xlsx" #leandro
#pbp_possessions.to_excel(path + file, sheet_name=match_ids[0], engine='xlsxwriter')

#print(pbp_possessions)


#print(match_pbp.columns)
#print(line_up(match_pbp))

#https://stackoverflow.com/questions/62419264/update-multiple-rows-in-mysql-with-pandas-dataframe/62422786#62422786
'''