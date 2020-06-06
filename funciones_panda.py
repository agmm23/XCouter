# IMPORTS
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

def match_pbp(df, match_ids):
    '''This function returns a DF with the PBP of the matches selected in the match_ids Series'''
    df_team = df.where( df['id_match'].isin(match_ids) ).dropna(how='all')
    return df_team

#print(match_pbp.__doc__)


def matches(df, team):
    '''This function returns the id_matchs of a team in the given df'''
    matches = df.where ( (df['team_name'] == team) | (df['team_rival'] == team) ).dropna(how='all')['id_match'].unique()
    return matches

#print(matches.__doc__)

def all_matches(df):
    '''This function returns all the id_matchs of the df'''
    matches = df['id_match'].unique()
    return matches

#print(all_matches.__doc__)

def stats_df(df):
    '''This function returns the Offensive Rebounds (ORB), Defensive Rebounds (DRB), Opponent ORB (OppORB), Opponent DRB (OppDRB), Turnovers (TO), Opponent Turnovers (OppTO),
Free Throw Attempts (FTA), Free Throws Made (FT), 2 Point Shot Attempts (2PTA), 2 Point Shots Made (2PT), 3 Point Shot Attempts (3PTA), 3 Point Shots Made (3PT),
Field Goal Attempted (FGA), Field Goals Made (FG), Total Points Scored (PTS), Percentage of Field Goals (FG%), Percentage of 2 Point Shots Made (2PT%),
Percentage of 3 Point Shots Made (3PT%)  for all the teams in the given PbP df.'''

    team = df['team_name'].unique()  # numpy.array
    stats = pd.DataFrame({'TEAM': team}).set_index('TEAM')
    opp = pd.DataFrame({'TEAM': team}).set_index('TEAM')

    stats['ORB'] = \
    df[((df['actionType_x'] == 'rebound') & (df['subType_x'] == 'offensive'))].groupby('team_name', sort=True)[
        'actionType_x'].count()
    stats['DRB'] = \
    df[((df['actionType_x'] == 'rebound') & (df['subType_x'] == 'defensive'))].groupby('team_name', sort=True)[
        'actionType_x'].count()

    stats['OppDRB'] = \
    df[((df['actionType_x'] == 'rebound') & (df['subType_x'] == 'defensive'))].groupby('team_rival', sort=True)[
        'actionType_x'].count()
    stats['OppORB'] = \
    df[((df['actionType_x'] == 'rebound') & (df['subType_x'] == 'offensive'))].groupby('team_rival', sort=True)[
        'actionType_x'].count()

    stats['TO'] = df[(df['actionType_x'] == 'turnover')].groupby('team_name', sort=True)['actionType_x'].count()
    stats['OppTO'] = df[(df['actionType_x'] == 'turnover')].groupby('team_rival', sort=True)['actionType_x'].count()

    stats['FTA'] = df[(df['actionType_x'] == 'freethrow')].groupby('team_name', sort=True)['actionType_x'].count()
    stats['OppFTA'] = df[(df['actionType_x'] == 'freethrow')].groupby('team_rival', sort=True)['actionType_x'].count()
    stats['FT'] = df[((df['actionType_x'] == 'freethrow') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType_x'].count()

    stats['2PTA'] = df[(df['actionType_x'] == '2pt')].groupby('team_name', sort=True)['actionType_x'].count()
    stats['2PT'] = df[((df['actionType_x'] == '2pt') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType_x'].count()

    stats['3PTA'] = df[(df['actionType_x'] == '3pt')].groupby('team_name', sort=True)['actionType_x'].count()
    stats['3PT'] = df[((df['actionType_x'] == '3pt') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType_x'].count()
    stats['Opp3PT'] = df[((df['actionType_x'] == '3pt') & (df['success'] == 1))].groupby('team_rival', sort=True)[
        'actionType_x'].count()

    stats['FGA'] = df[((df['actionType_x'].isin(['2pt', '3pt'])))].groupby('team_name', sort=True)[
        'actionType_x'].count()
    stats['OppFGA'] = df[((df['actionType_x'].isin(['2pt', '3pt'])))].groupby('team_rival', sort=True)[
        'actionType_x'].count()

    stats['FG'] = \
    df[((df['actionType_x'].isin(['2pt', '3pt'])) & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType_x'].count()
    stats['OppFG'] = \
    df[((df['actionType_x'].isin(['2pt', '3pt'])) & (df['success'] == 1))].groupby('team_rival', sort=True)[
        'actionType_x'].count()

    stats.fillna(0, inplace=True)  # por el boolean mask
    opp.fillna(0, inplace=True)
    # Attempted and Made Points
    # stats['PTSA'] = 3 * stats['3PTA'] + 2 * stats['2PTA'] + stats['FTA']
    stats['PTS'] = 3 * stats['3PT'] + 2 * stats['2PT'] + stats['FT']
    # Percentage of Field Goals Made
    stats['FG%'] = stats['FG'] / stats['FGA'] * 100
    # Ppercentage of 2 point shots made
    stats['2PT%'] = stats['2PT'] / stats['2PTA'] * 100
    # Percentage of 3 point shots made
    stats['3PT%'] = stats['3PT'] / stats['3PTA'] * 100

    #### FOUR FACTORS
    ## SHOOTING:
    # Effective Field Goal Percentage
    # This measure is a scale corrected measure to identify field goal percentage for a team.
    # With eFG% we do obtain the best relative measurement for points per field goal attempt; simple by multiplying by two.
    # accounts for made three pointers (3PM). isolates a player’s (or team’s) shooting efficiency from the field.
    stats['eFG%'] = (stats['FG'] + 0.5 * stats['3PT']) / stats['FGA']
    stats['OppeFG%'] = (stats['OppFG'] + 0.5 * stats['Opp3PT']) / stats['OppFGA']

    # True Shooting Percentage
    # accounts for both three pointers and free throws.
    # Provides a measure of total efficiency in scoring attempts, takes into account field goals, 3-point field goals, and free throws.
    stats['TS%'] = (stats['PTS'] / 2) / (stats['FGA'] + 0.44 * stats['FTA'])

    ## REBOUNDINGS: ORBP, DRBP (offensive and Defensive Rebound Percentage)
    stats['DREB%'] = stats['DRB'] / (stats['DRB'] + stats['OppORB'])
    stats['OREB%'] = stats['ORB'] / (stats['ORB'] + stats['OppDRB'])

    ## TURNOVER: Turnover Ratio
    # Turnover percentage is an estimate of turnovers per 100 plays. ( play = FGA + 0.44 * FTA + TO )
    stats['TOV%'] = 100 * stats['TO'] / (stats['FGA'] + 0.44 * stats['FTA'] + stats['TO'])
    stats['OppTOV%'] = 100 * stats['OppTO'] / (stats['OppFGA'] + 0.44 * stats['OppFTA'] + stats['OppTO'])

    ## FREE THROWS:
    # Field Throw Attempt
    stats['FTRate'] = stats['FTA'] / stats['FGA']
    stats['OppFTRate'] = stats['OppFTA'] / stats['OppFGA']

    return stats

print(stats_df.__doc__)



def orb(df, team):
    '''This function returns the ORB for a team'''
    orb = df[df.index.isin([team])]['ORB']
    return orb

def drb(df, team):
    '''This function returns the DRB  for a team:'''
    drb = df[df.index.isin([team])]['DRB']
    return drb

def opp_orb(df, team):
    '''This function returns the Opponent ORB'''
    opp_orb = df[df.index.isin([team])]['OppORB']
    return opp_orb

def opp_drb(df, team):
    '''This function returns the Opponent ORB'''
    opp_drb = df[df.index.isin([team])]['OppDRB']
    return opp_drb

def orebp(df, team):
    '''This function returns the ORB percentage (quality of a team’s ability to rebound) for a team:
    Number of offensive rebounds divided by the number of available rebounds after a missed field goal attempt'''
    orp = df[df.index.isin([team])]['OREB%']
    return orp

def drebp(df, team):    # (DR%)
    '''This function returns the ORB percentage (OREB%)for a team:
    Number of defensive rebounds divided by the number of opponent’s field goal misses that are available for rebound'''
    drp = df[df.index.isin([team])]['DREB%']
    return drp

def ftrate(df, team):    # (DR%)
    '''This function returns the FT Rate for a team:'''

    ftrate = df[df.index.isin([team])]['FTRate']
    return ftrate

#def to(df):
#    '''This function returns the ORB for a team in the given PBP df.'''
#    team = df['team_name'].unique()  # numpy.array
#  #  TURNOVER = pd.DataFrame({'TEAM': team}).set_index('TEAM')
#  #  TURNOVER['TO'] = df[ ( (df['actionType_x'] == 'rebound') & (df['subType_x'] == 'offensive') )].groupby('team_name', sort = True)['actionType_x'].count()
#
#
##SOURCES
#
###https://www.breakthroughbasketball.com/stats/definitions.html
##https://spatialjam.com/glossary

