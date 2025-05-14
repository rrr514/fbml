import pandas as pd

df = pd.read_csv('2023playerstats.csv')


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
    subdf.to_csv(f'2023playerstats_{pos}.csv', index=False)
    print(f"Data preprocessing complete. Processed data saved to '2023playerstats_{pos}.csv'.")

# Convert data frame to csv
# df.to_csv('2023playerstats_processed.csv', index=False)
# print("Data preprocessing complete. Processed data saved to '2023playerstats_processed.csv'.")