from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import time

def scrape_pfr_table(url: str) -> pd.DataFrame:
    """
    Scrapes a table from a Pro-Football-Reference URL using pandas.
    It correctly handles multi-level headers by joining them with an underscore
    to create prefixed column names (e.g., 'Passing_Yds').
    """
    try:
        # Use pandas to read the first table found on the page.
        # This is the standard and most robust method.
        df = pd.read_html(url)[0]
        
        # --- THIS IS THE FIX FOR MULTI-LEVEL HEADERS ---
        # Check if the columns are a MultiIndex (i.e., have multiple header rows)
        if isinstance(df.columns, pd.MultiIndex):
            # Join the levels of the MultiIndex to create single, prefixed column names.
            # If a header level is 'Unnamed', we discard it to avoid prefixes like 'Unnamed_0_level_0_Rk'.
            new_cols = []
            for col in df.columns.values:
                if 'Unnamed' in col[0]:
                    # If the top-level header is 'Unnamed', just use the second-level header
                    new_cols.append(col[1])
                else:
                    # Otherwise, join the levels with an underscore
                    new_cols.append('_'.join(col).strip())
            df.columns = new_cols
        
        # Remove the intermittent header rows that PFR includes in the table body
        df = df[df['Rk'] != 'Rk'].reset_index(drop=True)
        
        for i, player in enumerate(df['Player']):
            if not player:
                continue
            # Check if player name ends with +
            if player.endswith('+'):
                player = player[:-1]
                df.at[i, 'FirstTeamAllPro'] = 1
            
            # Chec if player name ends with *
            if player.endswith('*'):
                player = player[:-1]
                df.at[i, 'SelectedToProBowl'] = 1

            df.at[i, 'Player'] = player

        df = df.drop_duplicates(subset='Player', keep='first')
            
        return df
    except Exception as e:
        print(f"Error scraping or processing URL {url}: {e}")
        return pd.DataFrame()

def main():
    parser = argparse.ArgumentParser(description="Scrape player stats by year")
    parser.add_argument("year", type=int, help="Season year to scrape")

    args = parser.parse_args()

    year = args.year

    fantasy_url = "https://www.pro-football-reference.com/years/{}/fantasy.htm".format(year)
    adv_rec_url = f"https://www.pro-football-reference.com/years/{year}/receiving_advanced.htm"
    adv_rush_url = f"https://www.pro-football-reference.com/years/{year}/rushing_advanced.htm"
    adv_pass_url = f"https://www.pro-football-reference.com/years/{year}/passing_advanced.htm"

    print("1/4: Scraping Fantasy stats...")
    fantasy_df = scrape_pfr_table(fantasy_url)
    time.sleep(1)

    print("2/4: Scraping Advanced Receiving stats...")
    adv_rec_df = scrape_pfr_table(adv_rec_url)
    adv_rec_df = adv_rec_df.drop(columns=['Rk', 'Team', 'Age', 'Pos', 'G', 'GS'])
    time.sleep(1)

    print("3/4: Scraping Advanced Rushing stats...")
    adv_rush_df = scrape_pfr_table(adv_rush_url)
    adv_rush_df = adv_rush_df.drop(columns=['Rk', 'Team', 'Age', 'Pos', 'G', 'GS', 'Awards'])
    time.sleep(1)

    print("4/4: Scraping Advanced Passing stats...")
    adv_pass_df = scrape_pfr_table(adv_pass_url)
    adv_pass_df = adv_pass_df.drop(columns=['Rk', 'Team', 'Age', 'Pos', 'G', 'GS', 'Awards'])

    print("Merging all dataframes...")
    final_df = fantasy_df
    final_df = pd.merge(final_df, adv_pass_df, on='Player', how='left', suffixes=('', '_pass'))
    final_df = pd.merge(final_df, adv_rush_df, on='Player', how='left', suffixes=('', '_rush'))
    final_df = pd.merge(final_df, adv_rec_df, on='Player', how='left', suffixes=('', '_rec'))

    final_df['Year'] = year

    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', '{}playerstats.csv'.format(year))

    final_df.to_csv(filepath, index=False)
    print(f"Player data for the year {year} has been created and saved to: {filepath}")

if __name__ == '__main__':
    main()