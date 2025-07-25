import pandas as pd
import argparse
import os
import sys

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Preprocess fantasy football stats by year")
parser.add_argument("year", type=int, help="Season year to process")

args = parser.parse_args()

year = args.year

fantasy_csv = os.path.join('data', f'{year}playerstats.csv')

if not os.path.exists(fantasy_csv):
    print(f"Error: Input file not found at '{fantasy_csv}'")
    print("Please make sure that you have scraped the data before preprocessing it")
    sys.exit(1)

fantasy_df = pd.read_csv(fantasy_csv)

# Keeping for backwards compatibility
rename_mapping = {
    'Tm': 'Team',
    'Games_G': 'GamesPlayed',
    'Games_GS': 'GamesStarted',
    'Passing_Cmp': 'PassCmp',
    'Passing_Att': 'PassAtt',
    'Passing_Yds': 'PassYds',
    'Passing_TD': 'PassTD',
    'Passing_Int': 'PassInt',
    'Rushing_Att': 'RushAtt',
    'Rushing_Yds': 'RushYds',
    'Rushing_Y/A': 'RushYdsPerAtt',
    'Rushing_TD': 'RushTD',
    'Receiving_Tgt': 'Targets',
    'Receiving_Rec': 'Receptions',
    'Receiving_Yds': 'RecYds',
    'Receiving_Y/R': 'RecYdsPerReception',
    'Receiving_TD': 'RecTD',
    'Fumbles_Fmb': 'Fumbles',
    'Fumbles_FL': 'FumblesLost',
    'Scoring_TD': 'TotalTD',
    'Scoring_2PM': 'TwoPtConvMade',
    'Scoring_2PP': 'TwoPtConvPassing',
    'Fantasy_FantPt': 'FantasyPts',
    'Fantasy_PPR': 'FantasyPtsPPR',
    'Fantasy_DKPt': 'FantasyPtsDraftKings',
    'Fantasy_FDPt': 'FantasyPtsFanDuel',
    'Fantasy_VBD': 'VBD',
    'Fantasy_PosRank': 'PosRank',
    'Fantasy_OvRank': 'OverallRank',
}

fantasy_df.rename(columns=rename_mapping, inplace=True)


# # One hot encode the 'Team' column
# fantasy_df = pd.get_dummies(fantasy_df, columns=['Team'], prefix='Team', drop_first=True)

# Replace NAN in FantasyPts
fantasy_df['FantasyPts'] = fantasy_df['FantasyPts'].fillna(0)
# Replace NAN in FantasyPtrPPR
fantasy_df['FantasyPtsPPR'] = fantasy_df['FantasyPtsPPR'].fillna(0)
# Replace NAN in FantasyPtsDraftKings
fantasy_df['FantasyPtsDraftKings'] = fantasy_df['FantasyPtsDraftKings'].fillna(0)
# Replace NAN in FantasyPtsFanDuel
fantasy_df['FantasyPtsFanDuel'] = fantasy_df['FantasyPtsFanDuel'].fillna(0)


# Split data frame into 4 sub data frames based on position
dfs = {}
for pos, subdf in fantasy_df.groupby('FantPos'):
    # Considering FBs and RBs as the same position
    if pos in ['RB', 'FB']:
        dfs.setdefault('RB_FB', []).append(subdf)
    else:
        dfs[pos] = subdf.copy()
dfs['RB_FB'] = pd.concat(dfs['RB_FB'], ignore_index=True)


# Convert data frames to csvs
for pos, subdf in dfs.items():
    filepath = os.path.join('data', f'{year}playerstats_{pos}.csv')
    subdf.to_csv(filepath, index=False)
    print(f"Data preprocessing complete. Processed data saved to '{filepath}'.")
    
