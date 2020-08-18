from match_functions import *


#  lineup line_up

def line_up(match_pbp):
    #onCourt = match_pbp.groupby(['h1','h2','h3','h4','h5','v1','v2','v3','v4','v5'])
    #onCourt = match_pbp.groupby(['h1', 'h2', 'h3', 'h4', 'h5'])
    onCourt = match_pbp.groupby(['v1', 'v2', 'v3', 'v4', 'v5'])
    visitor = match_pbp.loc[0:,'v1':'v5'].values
    visitor.sort(axis=1)
    visitorsort = match_pbp(visitor, match_pbp.index, list(match_pbp.columns.values)[3:8])
    #return onCourt.groups
    return visitor #onCourt['v4'].count()
