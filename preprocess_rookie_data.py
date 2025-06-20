import pandas as pd
import argparse

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Preprocess fantasy football rookie stats by year")
parser.add_argument("--year", type=int, required=True, help="Season year to process")

args = parser.parse_args()

year = args.year
csv = f'{year}rookiestats.csv'
df = pd.read_csv(csv)

# Split data frame into 4 sub data frames based on position
dfs = {}
for pos, subdf in df.groupby('Pos'):
    if pos in ['RB', 'FB']:
        dfs.setdefault('RB_FB', []).append(subdf)
    else:
        dfs[pos] = subdf.copy()
dfs['RB_FB'] = pd.concat(dfs['RB_FB'], ignore_index=True)

for pos, subdf in dfs.items():
    subdf.to_csv(f'{year}rookiestats_{pos}.csv', index=False)
    print(f"Data preprocessing complete. Processed data saved to '{year}rookiestats_{pos}.csv'.")



