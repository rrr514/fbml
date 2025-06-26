import pandas as pd
import argparse
import os
import sys

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Preprocess fantasy football rookie stats by year")
parser.add_argument("--year", type=int, required=True, help="Season year to process")

args = parser.parse_args()

year = args.year
csv = os.path.join('data', f'{year}rookiestats.csv')

if not os.path.exists(csv):
    print(f"Error: Input file not found at '{csv}'")
    print("Please make sure that you have scraped the data before preprocessing it")
    sys.exit(1)

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
    filepath = os.path.join('data', f'{year}rookiestats_{pos}.csv')
    subdf.to_csv(filepath, index=False)
    print(f"Data preprocessing complete. Processed data saved to '{filepath}'.")



