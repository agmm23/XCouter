ACRONISMOS:
----------
AST: assist
STL: steal
BLK: block
xA: attempt
Oppx: opposite x

ORB: offensive rebound
DRB: defensive rebound

TO: turnover

FG: field goal (2pts y 3pts)
FGA%: percentage of FG made

PTS: points made

FOUR FACTORS:
eFG: effective FG%
# This measure is a scale corrected measure to identify field goal percentage for a team.
# With eFG% we do obtain the best relative measurement for points per field goal attempt; simple by multiplying by two.    # accounts for made three pointers (3PM). isolates a player’s (or team’s) shooting efficiency from the field.

TS%: true shooting %
# metric that factors a player’s or a team’s performance at the free-throw line and considers the efficiency on all types of shots.
# Provides a measure of total efficiency in scoring attempts, takes into account field goals, 3-point field goals and free throws.
TS% = (PTS / 2) / (FGA + 0.44 * FTA)


TOR: turnover ratio
#Turnover percentage is an estimate of turnovers per plays. ( play = FGA + 0.44 * FTA + TO ) (nota: La definición de la NBA incluye AST en denominador)
#Turnover Ratio/Percentage, is the percentage of a team’s possessions that end in a turnover.
TOR = TO/ [(FGA)+(0.44*FTA)+TO]   (la calculan x 100 - no multipliqué)

DRB% = DRB / (DRB + ORB)

FTRate: FT/FGA