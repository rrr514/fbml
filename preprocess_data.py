import pandas as pd
import argparse

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Preprocess fantasy football stats by year")
parser.add_argument("--year", type=int, required=True, help="Season year to process")

args = parser.parse_args()

year = args.year
csv = f'{year}playerstats.csv'
df = pd.read_csv(csv)


# Remove the first column
df = df.iloc[:, 1:]


# Renaming of columns
df.columns = ['Player', 'Team', 'FantPos', 'Age', 'GamesPlayed', 'GamesStarted', 
              'PassCmp', 'PassAtt', 'PassYds', 'PassTD', 'PassInt',
              'RushAtt', 'RushYds', 'RushYdsPerAtt', 'RushTD',
              'Targets', 'Receptions', 'RecYds', 'RecYdsPerReception', 'RecTD',
              'Fumbles', 'FumblesLost',
              'TotalTD', 'TwoPtConvMade', 'TwoPtConvPassing',
              'FantasyPts', 'FantasyPtsPPR', 'FantasyPtsDraftKings', 'FantasyPtsFanDuel', 'VBD', 'PosRank', 'OverallRank',
              'Year']


# Add column if player was selected to Pro Bowl/First Team All-Pro
df['SelectedToProBowl'] = 0
df['FirstTeamAllPro'] = 0

for i, player in enumerate(df['Player']):
    # Check if player name ends with +
    if player.endswith('+'):
        player = player[:-1]
        df.at[i, 'FirstTeamAllPro'] = 1
    
    # Chec if player name ends with *
    if player.endswith('*'):
        player = player[:-1]
        df.at[i, 'SelectedToProBowl'] = 1

    df.at[i, 'Player'] = player


# One hot encode the 'Team' column
df = pd.get_dummies(df, columns=['Team'], prefix='Team', drop_first=True)

# Replace NAN in FantasyPts
df['FantasyPts'] = df['FantasyPts'].fillna(0)
# Replace NAN in FantasyPtrPPR
df['FantasyPtsPPR'] = df['FantasyPtsPPR'].fillna(0)
# Replace NAN in FantasyPtsDraftKings
df['FantasyPtsDraftKings'] = df['FantasyPtsDraftKings'].fillna(0)
# Replace NAN in FantasyPtsFanDuel
df['FantasyPtsFanDuel'] = df['FantasyPtsFanDuel'].fillna(0)


# Split data frame into 4 sub data frames basd on position
dfs = {}
for pos, subdf in df.groupby('FantPos'):
    # Considering FBs and RBs as the same position
    if pos in ['RB', 'FB']:
        dfs.setdefault('RB_FB', []).append(subdf)
    else:
        dfs[pos] = subdf.copy()
dfs['RB_FB'] = pd.concat(dfs['RB_FB'], ignore_index=True)


# Convert data frames to csvs
for pos, subdf in dfs.items():
    subdf.to_csv(f'{year}playerstats_{pos}.csv', index=False)
    print(f"Data preprocessing complete. Processed data saved to '{year}playerstats_{pos}.csv'.")
