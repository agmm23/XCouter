import numpy as np
from match_functions import *


# def team_possessions(match_pbp, match_ids):  #match_id para guardar el archivo
#
#
#    # Elimino acciones que no cuentan para swap de tno
##    substitution = (match_pbp['actionType'] == 'substitution')
##    foul = ((match_pbp['actionType'] == 'foul') | (match_pbp['actionType'] == 'foulon'))
##    jumpball = ((match_pbp['actionType'] == 'jumpball') & (match_pbp['subType'].isin(['lost', 'startperiod'])))
##    #lost_jumpball = ( ( match_pbp['actionType'] == 'jumpball' ) & ( match_pbp['subType'] == 'lost' ) )
##    timeout = (match_pbp['actionType'] == 'timeout')
##    assist = (match_pbp['actionType'] == 'assist')
##    block = (match_pbp['actionType'] == 'block')
##    remove = (substitution | assist | block | foul | jumpball | timeout)
#    possessionChanges = match_pbp.loc[ ~((match_pbp['actionType'].isin(['substitution', 'timeout', 'assist', 'block'])) \
#             | ( ((match_pbp['actionType'] == 'jumpball') & (match_pbp['subType'].isin(['lost', 'startperiod']))) )\
#             | ((match_pbp['actionType'] == 'foul') | (match_pbp['actionType'] == 'foulon')) )]\
#        [['Clave', 'tno', 'team_name', 'period', 'actionType', 'subType', 'gt']]
#    # Creo df sin las acciones que no cuentan para swap de tno
#    #possessionChanges1 = match_pbp[~remove].dropna(how='all')\
#    #    [['Clave', 'tno', 'team_name', 'period', 'actionType', 'subType', 'gt']]  # .reset_index(drop=True)
#    #print(possessionChanges.equals(possessionChanges1)) #True
#
#    # Determino cuando termina una posesion
#    #1) turnoveer
#    turnover = (possessionChanges['actionType'] == 'turnover')
#    #2) missed field goal and free throws
#    fg_missed_pos = ((possessionChanges['actionType'].isin(['2pt', '3pt'])) &  \
#                    (possessionChanges['tno'].ne(possessionChanges['tno'].shift(-1))))
#    ft_missed_pos = (possessionChanges['actionType'].isin(['freethrow']) & \
#                    (possessionChanges['subType'].isin(['1of1', '2of2', '3of3'])) & \
#                        (possessionChanges['tno'].ne(possessionChanges['tno'].shift(-1))) & \
#                             (possessionChanges['actionType'].shift(-1) != 'period'))  # comparo con tno de proxima jugada
#
#
#    # period = possessionChanges1['period'].ne(possessionChanges1['period'].shift(-1))
#
#    possessionChanges['end'] = (turnover | fg_missed_pos | ft_missed_pos )
#
#    possessionChanges['pos_no'] = possessionChanges['end'].astype(int).cumsum()
#    possessionChanges['gt_sec'] = possessionChanges['gt'].apply(gt_to_sec)
#    # possessionChanges['gt'] = possessionChanges['gt'].apply(gt_to_sec)
#
#
#    #Calculo de tiempo de posesion
#    possessionChanges.loc[((possessionChanges['actionType'] == 'period') & (possessionChanges['subType'].isin(['start', 'end']))), 'end'] = True
#
#    #Dejo solo las entradas con fin de posesion en true, para poder contar tiempos
#    keep_true =  ( possessionChanges['end'] == True )
#
#    possessions = possessionChanges[keep_true].dropna(how='all')[['Clave','team_name','actionType','subType', 'period', 'gt','gt_sec','end','pos_no']] #.copy()
#    #print(possessions)
#    possessions['diff'] = (possessions['gt_sec'].shift(1) - possessions['gt_sec'])
#
#    #Elmino entradas period start y stop
#    keep =  ~( (possessions['actionType'] == 'period') & (possessions['subType'].isin(['start','end'])) )
#    possessions = possessions[keep].dropna(how='all')
#
#    #Paso de floating a integer
#    possessions['pos_sec'] = possessions['diff'].astype(int)
#    possessions['period'] = possessions['period'].astype(int)
#
#    possessions = possessions.reset_index(drop=True)
#
#    return(possessions)


def possession_end(match_pbp):
    '''Esta funcion devuelve df con las jugadas que finalizan una posesion y su duracion'''
    #Elimino accines que no afectan fin de posesión
    possessionChanges = match_pbp.loc[~((match_pbp['actionType'].isin(['substitution', 'timeout', 'assist', 'block'])) \
                                        | ((
                        (match_pbp['actionType'] == 'jumpball') & (match_pbp['subType'].isin(['lost', 'startperiod'])))) \
                                        | ((match_pbp['actionType'] == 'foul') | (
                        match_pbp['actionType'] == 'foulon')))] \
        [['Clave', 'tno', 'team_name', 'period', 'actionType', 'subType', 'gt', 'success']]

    # Determino cuando termina una posesion
    # 1) turnover
    turnover = (possessionChanges['actionType'] == 'turnover')

    # 2) successful field goal and free throws
    made_fg = ((possessionChanges['actionType'].isin(['2pt', '3pt'])) & \
           (possessionChanges['success'] == 1))
    made_ft = (possessionChanges['actionType'].isin(['freethrow']) & \
           (possessionChanges['subType'].isin(['1of1', '2of2', '3of3'])) & \
           (possessionChanges['success'] == 1))

    # 3) failed field goal and free throws and doesn't get the off rebound
    missed_fg = ((possessionChanges['actionType'].isin(['2pt', '3pt'])) &
                 (possessionChanges['success'] == 0) &
                (possessionChanges['actionType'].shift(-1) == 'rebound') & (possessionChanges['subType'].shift(-1) != 'offensive'))

    missed_ft = (possessionChanges['actionType'].isin(['freethrow']) &
                 (possessionChanges['success'] == 0) &
                 (possessionChanges['subType'].isin(['1of1', '2of2', '3of3'])) &
                 (possessionChanges['actionType'].shift(-1) == 'rebound') & (possessionChanges['subType'].shift(-1) != 'offensive'))

    # 4) period end
    period_end = (possessionChanges['actionType'].shift(-1) == 'period') & (possessionChanges['subType'].shift(-1) == 'end')

    possessionChanges['end'] = (turnover | made_fg | made_ft | missed_fg | missed_ft | period_end)

    possessionChanges['pos_no'] = possessionChanges['end'].astype(int).cumsum()
    possessionChanges['gt_sec'] = possessionChanges['gt'].apply(gt_to_sec)
    # possessionChanges['gt'] = possessionChanges['gt'].apply(gt_to_sec)




    # Calculo de tiempo de posesion:

    possessionChanges.loc[((possessionChanges['actionType'] == 'period') & ( possessionChanges['subType'].isin(['start', 'end']))), 'end'] = True

    # Dejo solo las entradas con fin de posesion en true, para poder contar tiempos
    keep_true = (possessionChanges['end'] == True)

    possessionChanges = possessionChanges[keep_true].dropna(how='all')[   \
        ['Clave', 'team_name', 'actionType', 'subType', 'period', 'success', 'gt', 'gt_sec', 'end',
         'pos_no']]  # .copy()

    #pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (
    #    pbp_possessions['subType'].isin(['start', 'end']))), 'pos_sec'] = np.NaN

    possessionChanges['diff'] = (possessionChanges['gt_sec'].shift(1) - possessionChanges['gt_sec'])
    # possessions= possessionChanges[['Clave','team_name','actionType','subType', 'period', 'gt','gt_sec','success','end','pos_no']]

    # Elmino entradas period start y stop
    #remove = ~((possessionChanges['actionType'] == 'period') & (possessionChanges['subType'].isin(['start', 'end'])))
    #remove = ~((possessionChanges['actionType'] == 'period') & (possessionChanges['subType'].isin(['start', 'end'])))
    #possessionChanges = possessionChanges[remove].dropna(how='all')

    #Calculo tiempo posesion
    possessionChanges['pos_sec'] = possessionChanges['diff']  #.astype(int)
    #possessionChanges['period'] = possessionChanges['period'].astype(int)


    possessionsChanges = possessionChanges.reset_index(drop=True)

    return (possessionChanges[
        ['Clave', 'team_name', 'actionType', 'subType', 'period', 'gt', 'gt_sec', 'success', 'end', 'pos_no', 'pos_sec']])


# def visualize_possessions(match_pbp, match_ids):
#   #Para visualizar las posesiones en el playbyplay (para analisis)
#   #del match_pbp_pos
#   possessionChanges = possession_end(match_pbp, match_ids)
#   #Hago left merge del playbyplay con el df que solo tiene las jugadas que cuentan para las posesiones
#   match_pbp_pos = pd.merge(match_pbp, possessionChanges, how="left", on=["Clave"])
#
#   match_pbp_pos = match_pbp_pos.rename(columns={"previousAction_x": "previousAction"})
#
#   match_pbp_pos['end'] = match_pbp_pos['end'].fillna(False)
#   match_pbp_pos['pos_no'] = match_pbp_pos['end'].astype(int).cumsum() #+ 1
#
#   match_pbp_pos = match_pbp_pos[['id_match', 'period', 'team_name', 'actionNumber', 'player', 'actionType', 'subType', 'previousAction', 'gt', 'gt_sec','tno', 'scoring', 'success', 'end', 'pos_no']]
#
#   return(match_pbp_pos)

def pbp_possessions_df(match_pbp):
    # Para visualizar las posesiones en el playbyplay
    # del match_pbp_pos #jupyter
    possessions = possession_end(match_pbp)[['Clave', 'end', 'gt_sec', 'pos_no', 'pos_sec']]
    # Hago left merge del playbyplay con el df que solo tiene las jugadas que cuentan para las posesiones
    pbp_possessions = pd.merge(match_pbp, possessions, how="left", on=["Clave"])

    pbp_possessions = pbp_possessions.rename(columns={"previousAction_x": "previousAction"})

    pbp_possessions['end'] = pbp_possessions['end'].fillna(False)
    # Elimino los end en true de period start y end para contar las posesiones
    pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (pbp_possessions['subType'].isin(['start', 'end']))), 'end'] = False

    pbp_possessions['pos_no'] = pbp_possessions['end'].astype(int).cumsum()  # + 1

    # segundos de la última posesion queda en el period end. cuando la ultima jugada fue un tiro errado,los segundos siguientes no se sabe a que equipo corresponde
    #pbp_possessions['pos_sec2'] = pbp_possessions['pos_sec']
    #pbp_possessions.loc[((pbp_possessions['end'] == False)  & (~pbp_possessions['actionType'].isin(['2pt','3pt','freethrow']))   \
    #                     (pbp_possessions['actionType'].shift(-1) == 'period') & (pbp_possessions['subType'].shift(-1) == 'end')), 'pos_sec2'] = \
    #    pbp_possessions['pos_sec2'].shift(-1)
    #elimino el True del end en period start y end para que no sume posesiones
    pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (pbp_possessions['subType'].isin(['start', 'end']))), 'pos_sec'] = np.NaN

    pbp_possessions = pbp_possessions[
        ['id_match', 'period', 'actionNumber', 'team_name', 'player', 'actionType', 'subType',
         'previousAction', 'gt', 'gt_sec', 'tno', 'scoring', 'success', 'end', 'pos_no', 'pos_sec']]

    return (pbp_possessions)

def team_posssessions(match_pbp, team):
    ''''Esta funcion calcula las posesiones de un equipo'''
    pbp_possessions = pbp_possessions_df(match_pbp)
    pbp_posssessions_team = pbp_possessions.where(pbp_possessions['team_name'] == team).dropna()
    #print(pbp_posssessions_team)
    pbp_posssessions_team['pos_no'] = pbp_posssessions_team['end'].astype(int).cumsum()

    return pbp_posssessions_team

def team_posssessions_qty(match_pbp, team):
    return team_posssessions(match_pbp, team)['pos_no'].count()


