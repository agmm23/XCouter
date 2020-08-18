import sqlalchemy as db
import pandas as pd

### DB FUNCTIONS

def scouter(query):
    '''Devuelve df con el resultado de la query a la base scouter.'''
    connect_string = 'mysql+mysqlconnector://root:monic.123@localhost:3306/scouter'
    engine = db.create_engine(connect_string, connect_args={'auth_plugin': 'mysql_native_password'})
    connection = engine.connect()
    results = connection.execute(query).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    return df

def match_pbp_df(df, match_ids):
    '''Esta función devuelve un df con el pbp de los partidos seleccionados en la Serie match_ids'''
    return df.where( df['id_match'].isin(match_ids) ).dropna(how='all')


#print(match_pbp.__doc__)


def matches(df, team):
    '''Esta función devuelve los id_matchs de un equipo consierados en el df'''
    return df.where ( (df['team_name'] == team) | (df['team_rival'] == team) ).dropna(how='all')['id_match'].unique()


#print(matches.__doc__)

def all_matches(df):
    '''Esta función devuelve un numpy array con todos los id_matchs del df'''
    return df['id_match'].unique()

def all_teams(df):
    '''This function returns a numpy array with all the teams of the df'''
    return df.where (df['team_name'] != "" ).dropna(how='all')['team_name'].unique()

#print(all_matches.__doc__)

def gt_to_sec(gt):
    '''Esta función devuelve el game time (gt) medido en segundos'''
    if pd.isna(gt)==True:
        return 0
    else:
        mins = int(gt.split(':')[0]) * 60
        secs = int(gt.split(':')[1])
        val = mins + secs
    return round(val, 1)


def player_pbp_df(match_pbp, team, player):
    '''Esta función devuelve df con las jugadas del player en el df match_pbp'''
    # Filtro por team, por si hubiera nombres de jugador repetidos.
    keep_team = ((match_pbp['team_name'] == team) | (match_pbp['team_rival'] == team))

    # return possessions_df[keep_scoring].dropna(how='all')['pos_no'].count()
    match_pbp = match_pbp[keep_team].dropna(how='all')

    return match_pbp.loc[
      #  match_pbp[['h1', 'h2', 'h3', 'h4', 'h5']].isin([player]).any(axis=1)]
        match_pbp[['a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5']].isin([player]).any(axis=1)]


