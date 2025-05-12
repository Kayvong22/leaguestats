import io
import os
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

# Initialize string to store all output
strPrompt = "Summarize the following information and turn it into a script to be used in a stephen a smith style nfl sports talkshow:\n"

# Merge team names into each dataframe
dfPassing = dfPassing.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfReceiving = dfReceiving.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfRushing = dfRushing.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')
dfDefense = dfDefense.merge(dfTeams[['teamId', 'teamNameFull']], on='teamId', how='left')

# Passing Analysis
output = "\nTop 5 Quarterbacks by Passer Rating:\n"
strPrompt += output
print(output)

passing_stats = dfPassing[['fullName', 'teamNameFull', 'passerRating', 'passYds', 'passTDs', 'passInts', 'passCompPct']] \
    .sort_values('passerRating', ascending=False).head()
strPrompt += str(passing_stats) + "\n"
print(passing_stats)

output = "\nMost Efficient Passers (min 20 attempts):\n"
strPrompt += output
print(output)

efficient_passers = dfPassing[dfPassing['passAtt'] >= 20][
    ['fullName', 'teamNameFull', 'passYdsPerAtt', 'passYdsPerGame', 'passCompPct']
].sort_values('passYdsPerAtt', ascending=False).head()
strPrompt += str(efficient_passers) + "\n"
print(efficient_passers)

# Receiving Analysis
output = "\nTop 5 Receivers by Yards:\n"
strPrompt += output
print(output)

receiving_stats = dfReceiving[['fullName', 'teamNameFull', 'recYds', 'recCatches', 'recTDs', 'recYdsPerGame']] \
    .sort_values('recYds', ascending=False).head()
strPrompt += str(receiving_stats) + "\n"
print(receiving_stats)

output = "\nMost Reliable Receivers (min 5 catches):\n"
strPrompt += output
print(output)

reliable_receivers = dfReceiving[dfReceiving['recCatches'] >= 5][
    ['fullName', 'teamNameFull', 'recCatchPct', 'recDrops', 'recYdsPerCatch']
].sort_values('recCatchPct', ascending=False).head()
strPrompt += str(reliable_receivers) + "\n"
print(reliable_receivers)

output = "\nYards After Catch Leaders:\n"
strPrompt += output
print(output)

yac_leaders = dfReceiving[['fullName', 'teamNameFull', 'recYdsAfterCatch', 'recYacPerCatch']] \
    .sort_values('recYdsAfterCatch', ascending=False).head()
strPrompt += str(yac_leaders) + "\n"
print(yac_leaders)

# Rushing Analysis
output = "\nTop 5 Rushers by Yards:\n"
strPrompt += output
print(output)

rushing_stats = dfRushing[['fullName', 'teamNameFull', 'rushYds', 'rushAtt', 'rushTDs', 'rushYdsPerGame']] \
    .sort_values('rushYds', ascending=False).head()
strPrompt += str(rushing_stats) + "\n"
print(rushing_stats)

output = "\nMost Explosive Runners (min 5 carries):\n"
strPrompt += output
print(output)

explosive_runners = dfRushing[dfRushing['rushAtt'] >= 5][
    ['fullName', 'teamNameFull', 'rushYdsPerAtt', 'rush20PlusYds', 'rushLongest']
].sort_values('rushYdsPerAtt', ascending=False).head()
strPrompt += str(explosive_runners) + "\n"
print(explosive_runners)

output = "\nBest at Breaking Tackles:\n"
strPrompt += output
print(output)

tackle_breakers = dfRushing[['fullName', 'teamNameFull', 'rushBrokenTackles', 'rushYdsAfterContact']] \
    .sort_values('rushBrokenTackles', ascending=False).head()
strPrompt += str(tackle_breakers) + "\n"
print(tackle_breakers)

# Team-level Analysis
output = "\nTeam Passing Yards per Game:\n"
strPrompt += output
print(output)

team_passing = dfPassing.groupby('teamNameFull').agg({
    'passYds': 'sum',
    'passTDs': 'sum',
    'passInts': 'sum',
    'passYdsPerGame': 'mean'
}).sort_values('passYds', ascending=False)
strPrompt += str(team_passing.head()) + "\n"
print(team_passing.head())

output = "\nTeam Rushing Yards per Game:\n"
strPrompt += output
print(output)

team_rushing = dfRushing.groupby('teamNameFull').agg({
    'rushYds': 'sum',
    'rushTDs': 'sum',
    'rushYdsPerGame': 'mean',
    'rushFum': 'sum'
}).sort_values('rushYds', ascending=False)
strPrompt += str(team_rushing.head()) + "\n"
print(team_rushing.head())

# Calculate total offense for each team
team_total_offense = pd.DataFrame({
    'Total_Yards': team_passing['passYds'] + team_rushing['rushYds'],
    'Total_TDs': team_passing['passTDs'] + team_rushing['rushTDs'],
    'Pass_Yards': team_passing['passYds'],
    'Rush_Yards': team_rushing['rushYds']
}).sort_values('Total_Yards', ascending=False)

output = "\nTeam Total Offense Rankings:\n"
strPrompt += output
print(output)
strPrompt += str(team_total_offense.head()) + "\n"
print(team_total_offense.head())

print("\n=== DEFENSIVE STATISTICS ===\n")

# Top tacklers (minimum 10 total tackles)
output = "\nTop Tacklers:\n-------------\n"
strPrompt += output
print(output)

top_tacklers = dfDefense[dfDefense['defTotalTackles'] >= 10].head(10)
for _, player in top_tacklers.iterrows():
    output = f"{player['fullName']}: {player['defTotalTackles']} total tackles\n"
    strPrompt += output
    print(output.rstrip())

# Top pass defenders (minimum 2 combined INTs/deflections)
output = "\nTop Pass Defenders:\n-----------------\n"
strPrompt += output
print(output)

dfDefense['passDefPlays'] = dfDefense['defInts'] + dfDefense['defDeflections']
top_pass_defenders = dfDefense[dfDefense['passDefPlays'] >= 2].sort_values('passDefPlays', ascending=False).head(10)
for _, player in top_pass_defenders.iterrows():
    output = f"{player['fullName']}: {player['defInts']} INTs, " \
             f"{player['defDeflections']} deflections, " \
             f"{player['defIntReturnYds']} INT return yards\n"
    strPrompt += output
    print(output.rstrip())

# Top pass rushers (minimum 2 sacks)
output = "\nTop Pass Rushers:\n----------------\n"
strPrompt += output
print(output)

top_rushers = dfDefense[dfDefense['defSacks'] >= 2].sort_values('defSacks', ascending=False).head(10)
for _, player in top_rushers.iterrows():
    output = f"{player['fullName']}: {player['defSacks']} sacks\n"
    strPrompt += output
    print(output.rstrip())

# Defensive Playmakers (TDs, forced fumbles, fumble recoveries)
output = "\nDefensive Playmakers:\n-------------------\n"
strPrompt += output
print(output)

dfDefense['bigPlays'] = dfDefense['defTDs'] + dfDefense['defForcedFum'] + dfDefense['defFumRec']
top_playmakers = dfDefense[dfDefense['bigPlays'] > 0].sort_values('bigPlays', ascending=False).head(10)
for _, player in top_playmakers.iterrows():
    output = f"{player['fullName']}: {int(player['defTDs'])} TDs, " \
             f"{int(player['defForcedFum'])} forced fumbles, " \
             f"{int(player['defFumRec'])} fumble recoveries\n"
    strPrompt += output
    print(output.rstrip())

# Calculate team defensive stats
output = "\nTeam Defense Rankings:\n--------------------\n"
strPrompt += output
print(output)
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
output = "\nOverall Team Defense (Points Allowed):\n"
strPrompt += output
print(output)

top_teams_points = team_defense.sort_values('defPts').head(5)  # Ascending for points (lower is better)
for _, team in top_teams_points.iterrows():
    output = f"{team['teamNameFull']}: {int(team['defPts'])} points allowed\n"
    strPrompt += output
    print(output.rstrip())

metrics = [
    ('defInts', 'Interceptions'),
    ('defSacks', 'Sacks'),
    ('defForcedFum', 'Forced Fumbles'),
    ('defSafeties', 'Safeties')
]

for metric, label in metrics:
    output = f"\nTop 5 Teams - {label}:\n"
    strPrompt += output
    print(output)
    top_teams = team_defense.sort_values(metric, ascending=False).head(5)
    for _, team in top_teams.iterrows():
        output = f"{team['teamNameFull']}: {int(team[metric])}\n"
        strPrompt += output
        print(output.rstrip())

# Save the prompt to a file
with open("stats_prompt.txt", "w") as f:
    f.write(strPrompt)

# Save dfTeams to csv
output_path = os.path.join(os.path.dirname(__file__), 'dfTeams.csv')
dfTeams.to_csv(output_path, index=False)
