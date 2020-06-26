import sqlalchemy as db
import pandas as pd

### DB FUNCTIONS

def pbp(query):
    # Conectar a la DB
    connect_string = 'mysql+mysqlconnector://root:monic.123@localhost:3306/scouter'
    engine = db.create_engine(connect_string, connect_args={'auth_plugin': 'mysql_native_password'})
    connection = engine.connect()
    results = connection.execute(query).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    return df

def match_pbp_df(df, match_ids):
    '''This function returns a DF with the PBP of the matches selected in the match_ids Series'''
    return df.where( df['id_match'].isin(match_ids) ).dropna(how='all')


#print(match_pbp.__doc__)


def matches(df, team):
    '''This function returns the id_matchs of a team in the given df'''
    return df.where ( (df['team_name'] == team) | (df['team_rival'] == team) ).dropna(how='all')['id_match'].unique()


#print(matches.__doc__)

def all_matches(df):
    '''This function returns all the id_matchs of the df'''
    return df['id_match'].unique()


#print(all_matches.__doc__)

def gt_to_sec(gt):
    '''This function returns the game time (gt) in seconds'''
    if pd.isna(gt)==True:
        return 0
    else:
        mins = int(gt.split(':')[0]) * 60
        secs = int(gt.split(':')[1])
        val = mins + secs
    return round(val, 1)

