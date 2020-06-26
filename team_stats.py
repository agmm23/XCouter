# IMPORTS
from match_functions import *


def stats_df(df):
    '''stats_df: This function returns the Assists (AST), Steals (STL), Blocks (BLK), Offensive Rebounds (ORB), Defensive Rebounds (DRB), Opponent ORB (OppORB), Opponent DRB (OppDRB), Turnovers (TO), Opponent Turnovers (OppTO),
Free Throw Attempts (FTA), Free Throws Made (FT), 2 Point Shot Attempts (2PTA), 2 Point Shots Made (2PT), 3 Point Shot Attempts (3PTA), 3 Point Shots Made (3PT),
Field Goal Attempted (FGA), Field Goals Made (FG), Total Points Scored (PTS), Percentage of Field Goals (FG%), Percentage of 2 Point Shots Made (2PT%),
Percentage of 3 Point Shots Made (3PT%)  for all the teams in the given PbP df.'''
    keep = (df['team_name'] != "")
    df= df[keep].dropna(how='all')

    team = df['team_name'].unique()  # numpy.array
    print(team)
    stats = pd.DataFrame({'TEAM': team}).set_index('TEAM')
    opp = pd.DataFrame({'TEAM': team}).set_index('TEAM')
    # Estadísticas basicas
    stats['AST'] = df[(df['actionType'] == 'assist')].groupby('team_name', sort=True)['actionType'].count()
    stats['STL'] = df[(df['actionType'] == 'steal')].groupby('team_name', sort=True)['actionType'].count()
    stats['BLK'] = df[(df['actionType'] == 'block')].groupby('team_name', sort=True)['actionType'].count()

    stats['2PTA'] = df[(df['actionType'] == '2pt')].groupby('team_name', sort=True)['actionType'].count()
    stats['2PT'] = df[((df['actionType'] == '2pt') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType'].count()

    stats['3PTA'] = df[(df['actionType'] == '3pt')].groupby('team_name', sort=True)['actionType'].count()
    stats['3PT'] = df[((df['actionType'] == '3pt') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType'].count()

    stats['FTA'] = df[(df['actionType'] == 'freethrow')].groupby('team_name', sort=True)['actionType'].count()
    stats['OppFTA'] = df[(df['actionType'] == 'freethrow')].groupby('team_rival', sort=True)['actionType'].count()
    stats['FT'] = df[((df['actionType'] == 'freethrow') & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType'].count()

    stats['ORB'] = \
    df[((df['actionType'] == 'rebound') & (df['subType'] == 'offensive'))].groupby('team_name', sort=True)[
        'actionType'].count()
    stats['DRB'] = \
    df[((df['actionType'] == 'rebound') & (df['subType'] == 'defensive'))].groupby('team_name', sort=True)[
        'actionType'].count()

    stats['OppDRB'] = \
    df[((df['actionType'] == 'rebound') & (df['subType'] == 'defensive'))].groupby('team_rival', sort=True)[
        'actionType'].count()
    stats['OppORB'] = \
    df[((df['actionType'] == 'rebound') & (df['subType'] == 'offensive'))].groupby('team_rival', sort=True)[
        'actionType'].count()

    stats['TO'] = df[(df['actionType'] == 'turnover')].groupby('team_name', sort=True)['actionType'].count()
    stats['OppTO'] = df[(df['actionType'] == 'turnover')].groupby('team_rival', sort=True)['actionType'].count()

    stats['Opp3PT'] = df[((df['actionType'] == '3pt') & (df['success'] == 1))].groupby('team_rival', sort=True)[
        'actionType'].count()

    stats['FGA'] = df[(df['actionType'].isin(['2pt', '3pt']))].groupby('team_name', sort=True)[
        'actionType'].count()
    stats['OppFGA'] = df[(df['actionType'].isin(['2pt', '3pt']))].groupby('team_rival', sort=True)[
        'actionType'].count()

    stats['FG'] = \
    df[(df['actionType'].isin(['2pt', '3pt']) & (df['success'] == 1))].groupby('team_name', sort=True)[
        'actionType'].count()
    stats['OppFG'] = \
    df[(df['actionType'].isin(['2pt', '3pt']) & (df['success'] == 1))].groupby('team_rival', sort=True)[
        'actionType'].count()

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
    # Provides a measure of total efficiency in scoring attempts, takes into account field goals, 3-point field goals and free throws.
    stats['TS%'] = (stats['PTS'] / 2) / (stats['FGA'] + 0.44 * stats['FTA'])

    ## REBOUNDINGS: ORBP, DRBP (offensive and Defensive Rebound Percentage)
    stats['DREB%'] = stats['DRB'] / (stats['DRB'] + stats['OppORB'])
    stats['OREB%'] = stats['ORB'] / (stats['ORB'] + stats['OppDRB'])

    ## TURNOVER: Turnover Ratio
    # Turnover percentage is an estimate of turnovers per plays. ( play = FGA + 0.44 * FTA + TO ) La definición de la NBA incluye AST en denominador
    stats['TOV%'] = stats['TO'] / (stats['FGA'] + 0.44 * stats['FTA'] + stats['TO'])
    stats['OppTOV%'] = stats['OppTO'] / (stats['OppFGA'] + 0.44 * stats['OppFTA'] + stats['OppTO'])

    ## FREE THROWS:
    # Field Throw Attempt
    stats['FTRate'] = stats['FTA'] / stats['FGA']
    stats['OppFTRate'] = stats['OppFTA'] / stats['OppFGA']

    return stats

#print(stats_df.__doc__)



def orb(df, team):
    '''This function returns the ORB for a team'''
    return df[df.index.isin([team])]['ORB']


def drb(df, team):
    '''This function returns the DRB  for a team:'''
    return df[df.index.isin([team])]['DRB']


def opp_orb(df, team):
    '''This function returns the Opponent ORB'''
    return df[df.index.isin([team])]['OppORB']


def opp_drb(df, team):
    '''This function returns the Opponent ORB'''
    return df[df.index.isin([team])]['OppDRB']


def orebp(df, team):
    '''This function returns the ORB percentage (quality of a team’s ability to rebound) for a team:
    Number of offensive rebounds divided by the number of available rebounds after a missed field goal attempt'''
    return df[df.index.isin([team])]['OREB%']


def drebp(df, team):    # (DR%)
    '''This function returns the ORB percentage (OREB%)for a team:
    Number of defensive rebounds divided by the number of opponent’s field goal misses that are available for rebound'''
    return df[df.index.isin([team])]['DREB%']


def ftrate(df, team):    # (DR%)
    '''This function returns the FT Rate for a team:'''
    return df[df.index.isin([team])]['FTRate']





##SOURCES
#
###https://www.breakthroughbasketball.com/stats/definitions.html
##https://spatialjam.com/glossary


