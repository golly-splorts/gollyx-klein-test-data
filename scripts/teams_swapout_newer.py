import subprocess
from pprint import pprint
import os
import json


season = 0
write = True


seasondir = f'season{season}'

def _make_path(filename):
    return os.path.join(seasondir, filename)

oldteamsfile = _make_path('old_teams.json')
newteamsfile = _make_path('new_teams.json')
teamsfile    = _make_path('teams.json')
schedulefile = _make_path('schedule.json')
bracketfile  = _make_path('bracket.json')
seasonfile   = _make_path('season.json')
postfile     = _make_path('postseason.json')
seedfile     = _make_path('seed.json')

with open(oldteamsfile, 'r') as f:
    oldteams = json.load(f)
    
with open(newteamsfile, 'r') as f:
    newteams = json.load(f)

if len(oldteams) != len(newteams):
    raise Exception(f"Error: mismatch in number of teams in {oldteamsfile} and {newteamsfile}")

# Strategy:
#
# SF/Monterey League -> Cold/Hot League
# Low/High Division -> Fire/Water Division


# Get leagues/divisions for old/new
get_divisions = lambda x: sorted(list({j['division'] for j in x}))

old_divisions = get_divisions(oldteams)
new_divisions = get_divisions(newteams)

get_leagues = lambda x: sorted(list({j['league'] for j in x}))

old_leagues = get_leagues(oldteams)
new_leagues = get_leagues(newteams)


# Add team abbrs to league/division bins
def teams_byld(teams):
    d = {}
    for team in teams:
        lea = team['league']
        div = team['division']
        if (lea,div) in d:
            d[(lea,div)] += [team]
        else:
            d[(lea,div)] = [team]
    return d

old_teams_byld = teams_byld(oldteams)
new_teams_byld = teams_byld(newteams)



# Create a final map for each team attribute.
# This is what's used to do the final swapout.
abbr_map = {}
name_map = {}
color_map = {}
league_map = {}
division_map = {}

# Now iterate by league and by division,
# and figure out the corresponding team abbrs (old and new).
# Add them to a final list of tuples of corresponding abbrs.
for old_lea, new_lea in zip(old_leagues, new_leagues):
    league_map[old_lea] = new_lea
    for old_div, new_div in zip(old_divisions, new_divisions):
        division_map[old_div] = new_div

        old_teams = old_teams_byld[(old_lea, old_div)]
        new_teams = new_teams_byld[(new_lea, new_div)]

        for old_team, new_team in zip(old_teams, new_teams):
            abbr_map[old_team['teamAbbr']] = new_team['teamAbbr']
            name_map[old_team['teamName']] = new_team['teamName']
            color_map[old_team['teamColor']] = new_team['teamColor']


subprocess.call(['cp', newteamsfile, teamsfile])


#####################

with open(schedulefile, 'r') as f:
    schedule = json.load(f)

for day in schedule:
    for game in day:
        for i in range(2):
            name_key = f"team{i+1}Name"
            name_val = game[name_key]
            game[name_key] = name_map[name_val]

            abbr_key = f"team{i+1}Abbr"
            abbr_val = game[abbr_key]
            game[abbr_key] = abbr_map[abbr_val]

            color_key = f"team{i+1}Color"
            try:
                color_val = game[color_key]
                game[color_key] = color_map[color_val]
            except KeyError:
                pass

            lea_key = "league"
            try:
                lea_val = game[lea_key]
                game[lea_key] = league_map[lea_val]
            except KeyError:
                pass

if write:
    with open(schedulefile, 'w') as f:
        json.dump(schedule, f, indent=4)

#####################

with open(seasonfile, 'r') as f:
    season = json.load(f)

for day in season:
    for game in day:
        for i in range(2):
            name_key = f"team{i+1}Name"
            name_val = game[name_key]
            game[name_key] = name_map[name_val]

            abbr_key = f"team{i+1}Abbr"
            abbr_val = game[abbr_key]
            game[abbr_key] = abbr_map[abbr_val]

            color_key = f"team{i+1}Color"
            color_val = game[color_key]
            game[color_key] = color_map[color_val]

            lea_key = "league"
            try:
                lea_val = game[lea_key]
                game[lea_key] = league_map[lea_val]
            except KeyError:
                pass


if write:
    with open(seasonfile, 'w') as f:
        json.dump(season, f, indent=4)

#####################

with open(bracketfile, 'r') as f:
    bracket = json.load(f)

for series in bracket:
    miniseason = bracket[series]
    for day in miniseason:
        for game in day:
            for i in range(2):
                name_key = f"team{i+1}Name"
                name_val = game[name_key]
                if name_val in name_map:
                    game[name_key] = name_map[name_val]

                abbr_key = f"team{i+1}Abbr"
                abbr_val = game[abbr_key]
                if abbr_val in abbr_map:
                    game[abbr_key] = abbr_map[abbr_val]

                color_key = f"team{i+1}Color"
                try:
                    color_val = game[color_key]
                    game[color_key] = color_map[color_val]
                except KeyError:
                    pass

                lea_key = "league"
                try:
                    lea_val = game[lea_key]
                    game[lea_key] = league_map[lea_val]
                except KeyError:
                    pass

if write:
    with open(bracketfile, 'w') as f:
        json.dump(bracket, f, indent=4)

#####################

with open(postfile, 'r') as f:
    postseason = json.load(f)

for series in postseason:
    miniseason = postseason[series]
    for day in miniseason:
        for game in day:
            for i in range(2):
                name_key = f"team{i+1}Name"
                name_val = game[name_key]
                game[name_key] = name_map[name_val]

                abbr_key = f"team{i+1}Abbr"
                abbr_val = game[abbr_key]
                game[abbr_key] = abbr_map[abbr_val]

                color_key = f"team{i+1}Color"
                color_val = game[color_key]
                game[color_key] = color_map[color_val]

                lea_key = "league"
                try:
                    lea_val = game[lea_key]
                    game[lea_key] = league_map[lea_val]
                except KeyError:
                    pass

if write:
    with open(postfile, 'w') as f:
        json.dump(postseason, f, indent=4)

#####################

with open(seedfile, 'r') as f:
    seed = json.load(f)

newseed = {}
for league in seed:
    seeds = seed[league]

    newseeds = []
    for team_name in seeds:
        newseeds.append(name_map[team_name])

    newleague = league_map[league]
    newseed[newleague] = newseeds

if write:
    with open(seedfile, 'w') as f:
        json.dump(seed, f, indent=4)
