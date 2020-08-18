import numpy as np
from match_functions import *

def match_possessions_end(match_pbp):
    '''Esta funcion devuelve df con las jugadas que finalizan una posesion, así como su duracion, para las jugads conendidas en el df match_pbp'''
    #Elimino acciones que no afectan fin de posesión
    ## possessionChanges = match_pbp.loc[~((match_pbp['actionType'].isin(['substitution', 'timeout', 'assist', 'block'])) \
    possessionChanges = match_pbp.loc[~((match_pbp['actionType'].isin(['substitution', 'timeout', 'assist', 'block', 'period', 'game'])) \
            | ((
                        (match_pbp['actionType'] == 'jumpball') & (match_pbp['subType'].isin(['lost', 'startperiod'])))) \
                                        | ((match_pbp['actionType'] == 'foul') | (
                        match_pbp['actionType'] == 'foulon')))] \
        [['Clave', 'team_name', 'id_match','period', 'actionType', 'subType', 'gt', 'success', 'scoring']]

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

    # 4) period end - no cae nunca porque se elimino period end
    # period_end = (possessionChanges['actionType'].shift(-1) == 'period') & (possessionChanges['subType'].shift(-1) == 'end')

    # por si dataframe de partidos no incluye el period end
    change_period = (possessionChanges['period'] != possessionChanges['period'].shift(-1))

    match_change = (possessionChanges['id_match'] != possessionChanges['id_match'].shift(-1))

    possessionChanges['end'] = (turnover | made_fg | made_ft | missed_fg | missed_ft | change_period | match_change )

    ####---possessionChanges['end'] = (turnover | made_fg | made_ft | missed_fg | missed_ft | period_end)

    possessionChanges['pos_no'] = possessionChanges['end'].astype(int).cumsum()
    possessionChanges['gt_sec'] = possessionChanges['gt'].apply(gt_to_sec)
    # possessionChanges['gt'] = possessionChanges['gt'].apply(gt_to_sec)

    #Determino si posesion termino en tanto

    # Calculo de tiempo de posesion:
    # esto no va más porqu e se elimina period
    # possessionChanges.loc[((possessionChanges['actionType'] == 'period') & ( possessionChanges['subType'].isin(['start', 'end']))), 'end'] = True

    # Dejo solo las entradas con fin de posesion en true, para poder contar tiempos
    keep_true = (possessionChanges['end'] == True)

    possessionChanges = possessionChanges[keep_true].dropna(how='all')[   \
        ['Clave', 'team_name', 'id_match', 'actionType', 'subType', 'period', 'success', 'scoring', 'gt', 'gt_sec', 'end',
         'pos_no']]  # .copy()

    #pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (
    #    pbp_possessions['subType'].isin(['start', 'end']))), 'pos_sec'] = np.NaN

    # Calculo tiempo posesion
    #possessionChanges['diff'] = (possessionChanges['gt_sec'].shift(1) - possessionChanges['gt_sec'])
    possessionChanges['pos_sec'] = (possessionChanges['gt_sec'].shift(1) - possessionChanges['gt_sec'])
    # seteo primero
    possessionChanges.reset_index(inplace=True)
    start_time = possessionChanges.at[0, 'gt_sec']
    print(start_time)

    possessionChanges.loc[possessionChanges['pos_sec'] < 0, 'pos_sec'] = 600 - possessionChanges['gt_sec']
    possessionChanges.at[0, 'pos_sec'] = 600 - possessionChanges.at[0, 'gt_sec']


    # possessionChanges.loc[((possessionChanges['actionType'] == 'period') & (
    #    possessionChanges['subType'].isin(['start', 'end']))), 'end'] = True

    # possessions= possessionChanges[['Clave','team_name','actionType','subType', 'period', 'gt','gt_sec','success','end','pos_no']]

    # Elmino entradas period start y stop
    #remove = ~((possessionChanges['actionType'] == 'period') & (possessionChanges['subType'].isin(['start', 'end'])))
    #remove = ~((possessionChanges['actionType'] == 'period') & (possessionChanges['subType'].isin(['start', 'end'])))
    #possessionChanges = possessionChanges[remove].dropna(how='all')

    #Calculo tiempo posesion
    #possessionChanges['pos_sec'] = possessionChanges['diff']  #.astype(int)
    #possessionChanges['period'] = possessionChanges['period'].astype(int)


    possessionsChanges = possessionChanges.reset_index(drop=True)

    #debug
    #file = r"c:/Users/Monic/Documents/GitHub/XCouter/posesiones/1485999_end_org.xlsx"
    #possessionsChanges.to_excel(file, engine='xlsxwriter')
    #fin debug
    print(possessionChanges.head(15))

    return (possessionChanges[
        ['Clave', 'team_name', 'id_match', 'actionType', 'subType', 'period', 'gt', 'gt_sec', 'success', 'scoring', 'end', 'pos_no', 'pos_sec']])


def pbp_possessions_df(match_pbp):
    # Para visualizar las posesiones en el playbyplay. llama al match_possessions_end y concatena
    # del match_pbp_pos #jupyter
    possessions = match_possessions_end(match_pbp)[['Clave', 'end', 'gt_sec', 'pos_no', 'pos_sec']]

    # Hago left merge del playbyplay con el df que solo tiene las jugadas que cuentan para las posesiones
    pbp_possessions = pd.merge(match_pbp, possessions, how="left", on=["Clave"])

    pbp_possessions = pbp_possessions.rename(columns={"previousAction_x": "previousAction"})

    # Completo con FALSE los valores de end que quedan en NA por el merge
    pbp_possessions['end'] = pbp_possessions['end'].fillna(False)

    # Dejo en FALSE el campo end para period start y end para poder contar las posesiones
    pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (
        pbp_possessions['subType'].isin(['start', 'end']))), 'end'] = False

    # Calculo possession number. astype convierte true en 1 y false en 0
    pbp_possessions['pos_no'] = pbp_possessions['end'].astype(int).cumsum()  # + 1

    # segundos de la última posesion queda en el period end. cuando la ultima jugada fue un tiro errado,los segundos siguientes no se sabe a que equipo corresponde
    # pbp_possessions['pos_sec2'] = pbp_possessions['pos_sec']
    # pbp_possessions.loc[((pbp_possessions['end'] == False)  & (~pbp_possessions['actionType'].isin(['2pt','3pt','freethrow']))   \
    #                     (pbp_possessions['actionType'].shift(-1) == 'period') & (pbp_possessions['subType'].shift(-1) == 'end')), 'pos_sec2'] = \
    #    pbp_possessions['pos_sec2'].shift(-1)

    pbp_possessions.loc[((pbp_possessions['actionType'] == 'period') & (
        pbp_possessions['subType'].isin(['start', 'end']))), 'pos_sec'] = np.NaN

    # pbp_possessions = pbp_possessions[
    #    ['id_match', 'period', 'actionNumber', 'team_name', 'player', 'actionType', 'subType',
    #     'previousAction', 'gt', 'gt_sec', 'tno', 'scoring', 'success', 'end', 'pos_no', 'pos_sec']]

    pbp_possessions = pbp_possessions[
        ['id_match', 'period', 'actionNumber', 'team_name', 'player', 'actionType', 'subType',
         'previousAction', 'gt', 'gt_sec', 'tno', 'scoring', 'success', 'end', 'pos_no', 'pos_sec',
         'a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5']]

    return (pbp_possessions)


def team_posssessions_df(match_pbp, team):
    '''Esta funcion calcula las posesiones de un equipo dado df con el play by play del/los partidos'''
    pbp_possessions = pbp_possessions_df(match_pbp)
    pbp_posssessions_team = pbp_possessions.where(pbp_possessions['team_name'] == team).dropna()
    pbp_posssessions_team['pos_no'] = pbp_posssessions_team['end'].astype(int).cumsum()

    return pbp_posssessions_team

def team_possessions(match_pbp, team):
    '''Esta funcion calcula para un equipo la cantidad y tiempo medio de posesiones del play by play del df match_pbp
    Usa el team_possessions_df'''
    team_possession_qty = team_posssessions_df(match_pbp, team)['pos_no'].count()
    team_possession_mean = team_posssessions_df(match_pbp, team)['pos_sec'].mean()
    return (team_possession_qty, team_possession_mean)


def team_scoring_possessions_qty(match_pbp, team):
    '''Esta funcion calcula la cantidad de posesiones exitosas de un equipo dado df con play by play del/los partidos'''
    possessions_df = team_posssessions_df(match_pbp, team)
    keep_scoring = ((possessions_df['scoring'] == 1) & (possessions_df['success'] == 1))
    return possessions_df[keep_scoring].dropna(how='all')['pos_no'].count()



#def team_possessions_qty(match_pbp, team):
#    '''Esta funcion calcula la cantidad de posesiones de un equipo dado df con el play by play del/los partidos'''
#    return team_posssessions_df(match_pbp, team)['pos_no'].count()

#def team_possessions_mean(match_pbp, team):
#    '''Esta funcion calcula el tiempo promedio de posesiones de un equipo dado el df match_pbp'''
#    return team_posssessions_df(match_pbp, team)['pos_sec'].mean()






#https://captaincalculator.com/sports/basketball/pace-factor-calculator/


