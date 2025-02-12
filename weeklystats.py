# weeklystats

import json
import pandas as pd
pd.set_option('display.max_columns', None)
###########################################
# get teams ids, names & organize rosters #
###########################################
with open("/Users/kayvon/Projects/madden_stats/leaguestats/teams.json", "r") as file:
    teams = json.load(file) 
file.close()

dfTeams = pd.DataFrame()
dfRosters = pd.DataFrame()

for team_key in teams.keys():
    # team info
    team = teams[team_key]
    teamId = int(team_key)
    abbrName = team.get('abbrName')
    cityName = team.get('cityName')
    teamName = team.get('teamName')
    divName = team.get('divName')

    row = {
        'teamId': teamId,
        'abbrName': abbrName,
        'cityName': cityName,
        'teamName': teamName,
        'divName': divName,
    }

    dfTeams = pd.concat(
        [dfTeams, pd.DataFrame([row])],
        ignore_index=True
    )

    # adding all roster data to dict
    roster = team.get('roster')
    
    for player_key in roster.keys():
        playerId = player_key
        player = roster[player_key]

        # add playerId for df
        player = {
            'teamId': int(teamId),
            'playerId': playerId,
            'playerName': player['firstName'] + ' ' + player['lastName'],
            **player
        }
        
        dfRosters = pd.concat(
            [dfRosters, pd.DataFrame([player])],
            ignore_index=True
        )

# add people's names
listPeople = [
    ['49ers', 'Ashwin'],
    ['Bears', 'Regy'],
    ['Bengals', 'Franco'],
    ['Monarchs', 'Nadeem'],
    ['Black Knights', 'Saba'],
    ['Browns', 'Mikey'],
    ['Buccaneers', 'Rohil'],
    ['Cardinals', 'Brett'],
    ['Chargers', 'Shawyon'],
    ['Chiefs', 'Ben'],
    ['Colts', 'N/A'],
    ['Commanders', 'Jaydeep'],
    ['Cowboys', 'Eddie'],
    ['Dolphins', 'Kunal'],
    ['Eagles', 'Devang'],
    ['Falcons', 'N/A'],
    ['Giants', 'Asad'],
    ['Jaguars', 'Kayvon'],
    ['Jets', 'Nafiz'],
    ['Lions', 'Will'],
    ['Packers', 'Aseem'],
    ['Panthers', 'Vishal'],
    ['Patriots', 'Feindy'],
    ['Raiders', 'Greyson'],
    ['Rams', 'Alishan'],
    ['Ravens', 'Komran'],
    ['Saints', 'Arnav'],
    ['Seahawks', 'Samin'],
    ['Steelers', 'Tyler'],
    ['Armadillos', 'Azim'],
    ['Titans', 'Zach'],
    ['Vikings', 'Sina']
    ]

dfTeams = dfTeams.merge(
    pd.DataFrame(listPeople, columns=['teamName', 'personName']),
    how='left',
    on='teamName',
)
# combine city and name for full team names
dfTeams['teamNameFull'] = dfTeams['cityName'] + ' ' + dfTeams['teamName'] + ' (' + dfTeams['personName'] + ')'

# add full team names to rosters
dfRosters = dfTeams.merge(
    dfRosters,
    how='left',
    on='teamId',
    )

# add home state names
listHomeStates = [
    [0, 'Alabama'],
    [1, 'Alaska'],
    [2, 'Arizona'],
    [3, 'Arkansas'],
    [4, 'California'],
    [5, 'Colorado'],
    [6, 'Connecticut'],
    [7, 'Delaware'],
    [8, 'Florida'],
    [9, 'Georgia'],
    [10, 'Hawaii'],
    [11, 'Idaho'],
    [12, 'Illinois'],
    [13, 'Indiana'],
    [14, 'Iowa'],
    [15, 'Kansas'],
    [16, 'Kentucky'],
    [17, 'Louisiana'],
    [18, 'Maine'],
    [19, 'Maryland'],
    [20, 'Massachusetts'],
    [21, 'Michigan'],
    [22, 'Minnesota'],
    [23, 'Mississippi'],
    [24, 'Missouri'],
    [25, 'Montana'],
    [26, 'Nebraska'],
    [27, 'Nevada'],
    [28, 'New Hampshire'],
    [29, 'New Jersey'],
    [30, 'New Mexico'],
    [31, 'New York'],
    [32, 'North Carolina'],
    [33, 'North Dakota'],
    [34, 'Ohio'],
    [35, 'Oklahoma'],
    [36, 'Oregon'],
    [37, 'Pennsylvania'],
    [38, 'Rhode Island'],
    [39, 'South Carolina'],
    [40, 'South Dakota'],
    [41, 'Tennessee'],
    [42, 'Texas'],
    [43, 'Utah'],
    [44, 'Vermont'],
    [45, 'Virginia'],
    [46, 'Washington'],
    [47, 'West Virginia'],
    [48, 'Wisconsin'],
    [49, 'Wyoming']
]
# change home states from index to full name
dfRosters = dfRosters.merge(
    pd.DataFrame(listHomeStates, columns=['homeState', 'homeStateName']),
    how='left',
    on='homeState',
)
# change 'playerId' type to int
dfRosters['playerId'] = dfRosters['playerId'].astype('int')

dfRostersClean = dfRosters[
    [
        'teamId', 
        'abbrName', 
        'cityName', 
        'teamName', 
        'divName', 
        'personName',
        'teamNameFull', 
        'playerId', 
        'firstName', 
        'lastName',
        'playerName',
        'homeStateName', 
        'homeTown', 
        'college', 
        'devTrait', 
        'age', 
    ]
]

del file, teams, roster, abbrName, cityName, divName, teamId, teamName, team_key, team, row, player_key, playerId, player, listPeople, listHomeStates

######################################
# Collect weekly stats for each team #
######################################
with open("/Users/kayvon/Projects/madden_stats/leaguestats/stats.json", "r") as file:
    stats = json.load(file)['reg']
file.close()

stats = stats[1:]

statsTeams = pd.DataFrame()
statsPlayers = pd.DataFrame()

for i in range(len(stats)):
    week = stats[i]
    if i != (len(stats)-1):
        if week is not None:
            for keyTeam in week.keys():
                statsTeams = pd.concat(
                    [statsTeams, pd.DataFrame([week[keyTeam]['team-stats']])],
                    ignore_index=True
                    )
                for keyPlayer in week[keyTeam]['player-stats'].keys():
                    statsPlayers = pd.concat(
                        [statsPlayers, pd.DataFrame(
                            [week[keyTeam]['player-stats'][keyPlayer]]
                            )],
                        ignore_index=True
                    )
    else:
        # this week vs all stats
        statsTeamsThisWeek = pd.DataFrame()
        statsPlayersThisWeek = pd.DataFrame()
        if week is not None:
            for keyTeam in week.keys():
                statsTeamsThisWeek = pd.concat(
                    [statsTeamsThisWeek, pd.DataFrame([week[keyTeam]['team-stats']])],
                    ignore_index=True
                    )
                for keyPlayer in week[keyTeam]['player-stats'].keys():
                    statsPlayersThisWeek = pd.concat(
                        [statsPlayersThisWeek, pd.DataFrame(
                            [week[keyTeam]['player-stats'][keyPlayer]]
                            )],
                        ignore_index=True
                    )

# sum all stats to get season stats vs last week stats

# add team names to df
statsTeams = statsTeams.merge(dfTeams, how='left', on='teamId')
# add player names & teams to df
statsPlayers = dfRosters[
    ['playerId', 'playerName', 'teamName', 'teamNameFull', 'position']
    ].merge(
        statsPlayers, 
        left_on='playerId', 
        right_on='rosterId'
        )

# add team names to df
statsTeamsThisWeek = statsTeamsThisWeek.merge(dfTeams, how='left', on='teamId')
# add player names & teams to df
statsPlayersThisWeek = dfRosters[
    ['playerId', 'playerName', 'teamName', 'teamNameFull', 'position']
    ].merge(
        statsPlayersThisWeek, 
        left_on='playerId', 
        right_on='rosterId'
        )






