import io
import json
import requests # type: ignore
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

# Read league teams data from JSON file
with open("../jsonfiles/madden_export_ps5_11476781_leagueteams.json", "r") as file:
    league_data = json.load(file)
    
# Create DataFrame from teams data
dfTeams = pd.DataFrame(league_data['leagueTeamInfoList'])

# Organize the DataFrame by division
dfTeams = dfTeams.sort_values(['divName', 'cityName']).reset_index(drop=True)

# add people's names
listPeople = [
    # AFC East
    ['Patriots', 'Feindy'],
    ['Monarchs', 'Nadeem'],
    ['Dolphins', 'Kunal'],
    ['Jets', 'Nafiz'],
    # AFC North
    ['Ravens', 'Komran'],
    ['Bengals', 'N/A'],
    ['Night Hawks', 'Mikey'],
    ['Snowhawks', 'Tyler'],
    # AFC South
    ['Condors', 'Raheem'],
    ['Jaguars', 'Kayvon'],
    ['Titans', 'Zach'],
    ['Armadillos', 'Azim'],
    # AFC West
    ['Shamrocks', 'Greyson'],
    ['Black Knights', 'Saba'],
    ['Wizards', 'Ben'],
    ['Chargers', 'Shawyon'],
    # NFC East
    ['Cowboys', 'David'],
    ['Eagles', 'Devang'],
    ['Commanders', 'Jaydeep'],
    ['Giants', 'Asad'], 
    # NFC North
    ['Bears', 'Regy'],
    ['Lions', 'Will'],
    ['Vikings', 'Sina'],
    ['Packers', 'Aseem'],
    # NFC South
    ['Falcons', 'Zain'],
    ['Buccaneers', 'Rohil'],
    ['Saints', 'Arnav'],
    ['Panthers', 'Vishal'],
    # NFC West
    ['49ers', 'Ashwin'],
    ['Rams', 'Alishan'],
    ['Cardinals', 'Brett'],
    ['Seahawks', 'Samin'],
    ]

# add people's names to teams
dfTeams = dfTeams.merge(
    pd.DataFrame(listPeople, columns=['displayName', 'personName']),
    how='left',
    on='displayName',
)
# combine city and name for full team names
dfTeams['teamNameFull'] = dfTeams['cityName'] + ' ' + dfTeams['displayName'] + ' (' + dfTeams['personName'] + ')'

# Read and process passing stats
with open("../jsonfiles/madden_export_ps5_11476781_week_reg_18_passing.json", "r") as file:
    passing_data = json.load(file)
    
# Create DataFrame from passing stats
dfPassing = pd.DataFrame(passing_data['playerPassingStatInfoList'])

# Convert numeric columns to appropriate types
numeric_columns = ['passerRating', 'passYds', 'passYdsPerGame', 'passCompPct', 
                  'passYdsPerAtt', 'passComp', 'passPts', 'passLongest', 
                  'passSacks', 'passInts', 'passAtt', 'passTDs']
                  
dfPassing[numeric_columns] = dfPassing[numeric_columns].apply(pd.to_numeric)

# Sort by passing yards descending
dfPassing = dfPassing.sort_values('passYds', ascending=False).reset_index(drop=True)

# Read and process receiving stats
with open("../jsonfiles/madden_export_ps5_11476781_week_reg_18_receiving.json", "r") as file:
    receiving_data = json.load(file)
    
# Create DataFrame from receiving stats
dfReceiving = pd.DataFrame(receiving_data['playerReceivingStatInfoList'])

# Convert numeric columns to appropriate types
numeric_columns = ['recYds', 'recYdsPerGame', 'recCatchPct', 'recYdsPerCatch',
                  'recCatches', 'recPts', 'recLongest', 'recTDs', 'recDrops',
                  'recYdsAfterCatch', 'recYacPerCatch', 'recToPct']

dfReceiving[numeric_columns] = dfReceiving[numeric_columns].apply(pd.to_numeric)

# Sort by receiving yards descending
dfReceiving = dfReceiving.sort_values('recYds', ascending=False).reset_index(drop=True)

# Read and process rushing stats
with open("../jsonfiles/madden_export_ps5_11476781_week_reg_18_rushing.json", "r") as file:
    rushing_data = json.load(file)
    
# Create DataFrame from rushing stats
dfRushing = pd.DataFrame(rushing_data['playerRushingStatInfoList'])

# Convert numeric columns to appropriate types
numeric_columns = ['rushYds', 'rushYdsPerGame', 'rushYdsPerAtt', 'rushAtt',
                  'rushTDs', 'rushLongest', 'rushYdsAfterContact', 'rushBrokenTackles',
                  'rushFum', 'rush20PlusYds', 'rushPts', 'rushToPct']

dfRushing[numeric_columns] = dfRushing[numeric_columns].apply(pd.to_numeric)

# Sort by rushing yards descending
dfRushing = dfRushing.sort_values('rushYds', ascending=False).reset_index(drop=True)

# Read and process defensive stats
with open("../jsonfiles/madden_export_ps5_11476781_week_reg_18_defense.json", "r") as file:
    defense_data = json.load(file)
    
# Create DataFrame from defensive stats
dfDefense = pd.DataFrame(defense_data['playerDefensiveStatInfoList'])

# Convert numeric columns to appropriate types
numeric_columns = ['defInts', 'defPts', 'defFumRec', 'defDeflections', 
                   'defSacks', 'defTDs', 'defSafeties', 'defTotalTackles',
                   'defCatchAllowed', 'defIntReturnYds', 'defForcedFum']

dfDefense[numeric_columns] = dfDefense[numeric_columns].apply(pd.to_numeric)

# Sort by total tackles descending
dfDefense = dfDefense.sort_values('defTotalTackles', ascending=False).reset_index(drop=True)

###########################################
# Analysis of Weekly and Season Statistics #
###########################################

# Merge team names into each dataframe
dfPassing = dfPassing.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfReceiving = dfReceiving.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfRushing = dfRushing.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfDefense = dfDefense.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')

# Passing Analysis
print("\nTop 5 Quarterbacks by Passer Rating:")
print(dfPassing[['fullName', 'teamNameFull', 'passerRating', 'passYds', 'passTDs', 'passInts', 'passCompPct']]
      .sort_values('passerRating', ascending=False).head())

print("\nMost Efficient Passers (min 20 attempts):")
efficient_passers = dfPassing[dfPassing['passAtt'] >= 20][
    ['fullName', 'teamNameFull', 'passYdsPerAtt', 'passYdsPerGame', 'passCompPct']
].sort_values('passYdsPerAtt', ascending=False).head()
print(efficient_passers)

# Receiving Analysis
print("\nTop 5 Receivers by Yards:")
print(dfReceiving[['fullName', 'teamNameFull', 'recYds', 'recCatches', 'recTDs', 'recYdsPerGame']]
      .sort_values('recYds', ascending=False).head())

print("\nMost Reliable Receivers (min 5 catches):")
reliable_receivers = dfReceiving[dfReceiving['recCatches'] >= 5][
    ['fullName', 'teamNameFull', 'recCatchPct', 'recDrops', 'recYdsPerCatch']
].sort_values('recCatchPct', ascending=False).head()
print(reliable_receivers)

print("\nYards After Catch Leaders:")
print(dfReceiving[['fullName', 'teamNameFull', 'recYdsAfterCatch', 'recYacPerCatch']]
      .sort_values('recYdsAfterCatch', ascending=False).head())

# Rushing Analysis
print("\nTop 5 Rushers by Yards:")
print(dfRushing[['fullName', 'teamNameFull', 'rushYds', 'rushAtt', 'rushTDs', 'rushYdsPerGame']]
      .sort_values('rushYds', ascending=False).head())

print("\nMost Explosive Runners (min 5 carries):")
explosive_runners = dfRushing[dfRushing['rushAtt'] >= 5][
    ['fullName', 'teamNameFull', 'rushYdsPerAtt', 'rush20PlusYds', 'rushLongest']
].sort_values('rushYdsPerAtt', ascending=False).head()
print(explosive_runners)

print("\nBest at Breaking Tackles:")
print(dfRushing[['fullName', 'teamNameFull', 'rushBrokenTackles', 'rushYdsAfterContact']]
      .sort_values('rushBrokenTackles', ascending=False).head())

# Team-level Analysis
print("\nTeam Passing Yards per Game:")
team_passing = dfPassing.groupby('teamNameFull').agg({
    'passYds': 'sum',
    'passTDs': 'sum',
    'passInts': 'sum',
    'passYdsPerGame': 'mean'
}).sort_values('passYds', ascending=False)
print(team_passing.head())

print("\nTeam Rushing Yards per Game:")
team_rushing = dfRushing.groupby('teamNameFull').agg({
    'rushYds': 'sum',
    'rushTDs': 'sum',
    'rushYdsPerGame': 'mean',
    'rushFum': 'sum'
}).sort_values('rushYds', ascending=False)
print(team_rushing.head())

# Calculate total offense for each team
team_total_offense = pd.DataFrame({
    'Total_Yards': team_passing['passYds'] + team_rushing['rushYds'],
    'Total_TDs': team_passing['passTDs'] + team_rushing['rushTDs'],
    'Pass_Yards': team_passing['passYds'],
    'Rush_Yards': team_rushing['rushYds']
}).sort_values('Total_Yards', ascending=False)

print("\nTeam Total Offense Rankings:")
print(team_total_offense.head())

print("\n=== DEFENSIVE STATISTICS ===\n")

# Top tacklers (minimum 10 total tackles)
print("\nTop Tacklers:")
print("-------------")
top_tacklers = dfDefense[dfDefense['defTotalTackles'] >= 10].head(10)
for _, player in top_tacklers.iterrows():
    print(f"{player['fullName']}: {player['defTotalTackles']} total tackles")

# Top pass defenders (minimum 2 combined INTs/deflections)
print("\nTop Pass Defenders:")
print("-----------------")
dfDefense['passDefPlays'] = dfDefense['defInts'] + dfDefense['defDeflections']
top_pass_defenders = dfDefense[dfDefense['passDefPlays'] >= 2].sort_values('passDefPlays', ascending=False).head(10)
for _, player in top_pass_defenders.iterrows():
    print(f"{player['fullName']}: {player['defInts']} INTs, "
          f"{player['defDeflections']} deflections, "
          f"{player['defIntReturnYds']} INT return yards")

# Top pass rushers (minimum 2 sacks)
print("\nTop Pass Rushers:")
print("----------------")
top_rushers = dfDefense[dfDefense['defSacks'] >= 2].sort_values('defSacks', ascending=False).head(10)
for _, player in top_rushers.iterrows():
    print(f"{player['fullName']}: {player['defSacks']} sacks")

# Defensive Playmakers (TDs, forced fumbles, fumble recoveries)
print("\nDefensive Playmakers:")
print("-------------------")
dfDefense['bigPlays'] = dfDefense['defTDs'] + dfDefense['defForcedFum'] + dfDefense['defFumRec']
top_playmakers = dfDefense[dfDefense['bigPlays'] > 0].sort_values('bigPlays', ascending=False).head(10)
for _, player in top_playmakers.iterrows():
    print(f"{player['fullName']}: {int(player['defTDs'])} TDs, "
          f"{int(player['defForcedFum'])} forced fumbles, "
          f"{int(player['defFumRec'])} fumble recoveries")

# Calculate team defensive stats
print("\nTeam Defense Rankings:")
print("--------------------")
team_defense = dfDefense.groupby('teamId').agg({
    'defTotalTackles': 'sum',
    'defSacks': 'sum',
    'defInts': 'sum',
    'defDeflections': 'sum',
    'defForcedFum': 'sum',
    'defFumRec': 'sum',
    'defTDs': 'sum',
    'defSafeties': 'sum',
    'defPts': 'sum',
    'defCatchAllowed': 'sum',
    'defIntReturnYds': 'sum'
}).reset_index()

# Merge with team names
team_defense = team_defense.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')

# Sort by various metrics and display rankings
print("\nOverall Team Defense (Points Allowed):")
top_teams_points = team_defense.sort_values('defPts').head(5)  # Ascending for points (lower is better)
for _, team in top_teams_points.iterrows():
    print(f"{team['teamNameFull']}: {int(team['defPts'])} points allowed")

metrics = [
    ('defInts', 'Interceptions'),
    ('defSacks', 'Sacks'),
    ('defForcedFum', 'Forced Fumbles'),
    ('defSafeties', 'Safeties')
]

for metric, label in metrics:
    print(f"\nTop 5 Teams - {label}:")
    top_teams = team_defense.sort_values(metric, ascending=False).head(5)
    for _, team in top_teams.iterrows():
        print(f"{team['teamNameFull']}: {int(team[metric])}")


