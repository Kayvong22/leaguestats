import pandas as pd
import os
import json
import glob
from typing import List, Dict, Any, Optional

def validate_player_data(player: Dict[str, Any]) -> bool:
    """Validate required fields are present in player data."""
    required_fields = ['rosterId', 'firstName', 'lastName', 'playerBestOvr', 'teamId']
    return all(field in player for field in required_fields)

def process_roster_file(file_path: str) -> List[Dict[str, Any]]:
    """Process a single roster file and return list of valid player data."""
    players = []
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if not data.get('success'):
            print(f"Warning: File {file_path} marked as unsuccessful")
            return players
            
        if 'rosterInfoList' not in data:
            print(f"Warning: No rosterInfoList in {file_path}")
            return players
            
        # Extract team ID from filename for team rosters
        team_id = None
        if 'team_' in file_path:
            team_id = file_path.split('team_')[1].split('_roster')[0]
            
        for player in data['rosterInfoList']:
            # For team rosters, verify teamId matches filename
            if team_id and str(player.get('teamId', '')) != team_id:
                continue
                
            if validate_player_data(player):
                players.append(player)
            else:
                print(f"Warning: Invalid player data found: {player.get('firstName', '')} {player.get('lastName', '')}")
                
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {str(e)}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        
    return players

def load_roster_data() -> Optional[pd.DataFrame]:
    """Load and process all roster files including team rosters and free agents."""
    json_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jsonfiles')
    all_players = []
    
    # Process team rosters
    roster_files = glob.glob(os.path.join(json_dir, '*team_*_roster.json'))
    print(f"Found {len(roster_files)} team roster files")
    
    # Process free agents roster
    fa_files = glob.glob(os.path.join(json_dir, '*freeagents_roster.json'))
    if fa_files:
        print("Found free agents roster file")
        roster_files.extend(fa_files)
    
    print(f"Processing {len(roster_files)} total roster files...")
    
    # Process each roster file
    for file_path in roster_files:
        players = process_roster_file(file_path)
        print(f"Processed {file_path}: found {len(players)} valid players")
        all_players.extend(players)
    
    if not all_players:
        print("Error: No valid player data found in any roster files.")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(all_players)
    
    # Add calculated columns
    df['full_name'] = df['firstName'] + ' ' + df['lastName']
    df['roster_type'] = df['teamId'].apply(lambda x: 'Free Agent' if x == 0 else 'Team Roster')
    
    # Sort by overall rating
    df = df.sort_values('playerBestOvr', ascending=False)

    dfTeams = pd.read_csv(os.path.join(os.path.dirname(__file__), 'dfTeams.csv'))

    df = pd.merge(
        dfTeams[['teamId', 'divName', 'displayName', 'teamNameFull']],
        df,
        how='right',
        on='teamId',
        )
    
    df = df[
        [
            'displayName',
            'teamNameFull',
            'full_name',
            'playerBestOvr',
            'devTrait',
            'age',
            'position',
            'speedRating',
            'accelRating',
            'height',
            'weight',
            'divName',
            'agilityRating',
            'awareRating',
            'bCVRating',
            'bigHitTrait',
            'birthDay',
            'birthMonth',
            'birthYear',
            'blockShedRating',
            'breakSackRating',
            'breakTackleRating',
            'cITRating',
            'capHit',
            'capReleaseNetSavings',
            'capReleasePenalty',
            'carryRating',
            'catchRating',
            'changeOfDirectionRating',
            'clutchTrait',
            'college',
            'confRating',
            'contractBonus',
            'contractLength',
            'contractSalary',
            'contractYearsLeft',
            'coverBallTrait',
            'dLBullRushTrait',
            'dLSpinTrait',
            'dLSwimTrait',
            'decisionMakerTrait',
            'desiredBonus',
            'desiredLength',
            'desiredSalary',
            'draftPick',
            'draftRound',
            'dropOpenPassTrait',
            'durabilityGrade',
            'experiencePoints',
            'feetInBoundsTrait',
            'fightForYardsTrait',
            'finesseMovesRating',
            'firstName',
            'hPCatchTrait',
            'highMotorTrait',
            'hitPowerRating',
            'homeState',
            'homeTown',
            'impactBlockRating',
            'injuryLength',
            'injuryRating',
            'injuryType',
            'intangibleGrade',
            'isActive',
            'isFreeAgent',
            'isOnIR',
            'isOnPracticeSquad',
            'jerseyNum',
            'jukeMoveRating',
            'jumpRating',
            'kickAccRating',
            'kickPowerRating',
            'kickRetRating',
            'lBStyleTrait',
            'lastName',
            'leadBlockRating',
            'legacyScore',
            'manCoverRating',
            'passBlockFinesseRating',
            'passBlockPowerRating',
            'passBlockRating',
            'penaltyTrait',
            'physicalGrade',
            'playActionRating',
            'playBallTrait',
            'playRecRating',
            'playerSchemeOvr',
            'portraitId',
            'posCatchTrait',
            'powerMovesRating',
            'predictTrait',
            'presentationId',
            'pressRating',
            'productionGrade',
            'pursuitRating',
            'qBStyleTrait',
            'reSignStatus',
            'releaseRating',
            'rookieYear',
            'rosterGoalList',
            'rosterId',
            'roster_type',
            'routeRunDeepRating',
            'routeRunMedRating',
            'routeRunShortRating',
            'runBlockFinesseRating',
            'runBlockPowerRating',
            'runBlockRating',
            'runStyle',
            'scheme',
            'sensePressureTrait',
            'signatureSlotList',
            'sizeGrade',
            'skillPoints',
            'specCatchRating',
            'spinMoveRating',
            'staminaRating',
            'stiffArmRating',
            'strengthRating',
            'stripBallTrait',
            'tackleRating',
            'teamId',
            'teamSchemeOvr',
            'throwAccDeepRating',
            'throwAccMidRating',
            'throwAccRating',
            'throwAccShortRating',
            'throwAwayTrait',
            'throwOnRunRating',
            'throwPowerRating',
            'throwUnderPressureRating',
            'tightSpiralTrait',
            'toughRating',
            'truckRating',
            'yACCatchTrait',
            'yearsPro',
            'zoneCoverRating'
        ]
    ]

    # Save to csv
    output_path = os.path.join(os.path.dirname(__file__), 'player_database.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\nProcess completed successfully:")
    print(f"Total players processed: {len(df)}")
    print(f"Team roster players: {len(df[df['roster_type'] == 'Team Roster'])}")
    print(f"Free agents: {len(df[df['roster_type'] == 'Free Agent'])}")
    print(f"Player database saved to {output_path}")
    
    return df

if __name__ == "__main__":
    df = load_roster_data()
