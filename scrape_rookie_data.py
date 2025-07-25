from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import time
from enum import Enum
import os


class Position(Enum):
    QB = "passing"
    RB = "rushing"
    FB = "rushing"
    WR = "receiving"
    TE = "receiving"

def extract_college_position_stats(soup, url, college_career_stats, pos):
    # Extract passing stats
    pos = pos.value
    found_stats = True
    table = soup.find('table', id=pos+'_standard')
    if not table:
        # print(f"Could not find", pos + f"_standard table at {url}")
        found_stats = False
    else:    
        tfoot = table.find('tfoot')
        if not tfoot:
            # print(f"Could not find tfoot in", pos + f"_standard table at {url}")
            found_stats = False
        else: 
            career_row = None
            career_row_id = f"{table.get('id', pos+'_standard')}.Career"
            career_row = tfoot.find('tr', id=career_row_id)

            if not career_row:
                print("Manual search for", pos, "career row")
                for row_in_footer in tfoot.find_all('tr'):
                    first_header_cell = row_in_footer.find('th')
                    if first_header_cell and 'Career' in first_header_cell.get_text(strip=True):
                        career_row = row_in_footer
                        break
            
            if not career_row:
                # print(f"Could not find", pos + f"_table Career row in table footer at {url}")
                found_stats = False
    
    if(found_stats is True):
        # Extract all data-stat attributes from the pos career row
        non_data_labels = ["year_id", "pos" , "awards"]
        for cell in career_row.find_all(['th', 'td']):
            if cell.has_attr('data-stat'):
                stat_label = cell['data-stat']
                stat_value = cell.get_text(strip = True)

                # Skip all non data labels
                if stat_label in non_data_labels: 
                    continue
                
                # Attempt to cast stat_value to a float
                try:
                    stat_value = float(stat_value)
                except ValueError:
                    print("ValueError in extract_college_position_stats() when trying to cast attribute", stat_label, "with value", stat_value, "to a float. Setting value to pd.NA")
                    stat_value = pd.NA
                
                column_name = f"Coll_{stat_label}"
                college_career_stats[column_name] = stat_value


def extract_college_career_stats(url):
    if not url or not isinstance(url, str) or not url.startswith('http'):
        print(f"Invalid or missing URL: {url}")
        return {}
    
    print(f"Fetching college data from: {url}")
    college_career_stats = {}
    html = urlopen(url)
    soup = BeautifulSoup(html, features="lxml")

    extract_college_position_stats(soup, url, college_career_stats, Position.QB)
    extract_college_position_stats(soup, url, college_career_stats, Position.RB)
    extract_college_position_stats(soup, url, college_career_stats, Position.WR)
     
    return college_career_stats




parser = argparse.ArgumentParser(description="Scrape rookie stats by year")
parser.add_argument("year", type=int, help="Season year to scrape")

args = parser.parse_args()

year = args.year

url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
html = urlopen(url)
soup = BeautifulSoup(html, features="lxml")

headers = [th.getText() for th in soup.findAll("tr")[1].findAll("th")]
headers = headers[1:]

rows = soup.findAll("tr", class_ = lambda table_rows: table_rows != "thead")
player_stats = []
for i in range(len(rows)):
    td_elements = rows[i].findAll("td")

    current_row_values = []
    for j, td_tag in enumerate(td_elements):
        # Extract out the URL to get college stats
        if j == len(td_elements) - 1:
            anchor_tag = td_tag.find('a')
            if anchor_tag and anchor_tag.has_attr('href'):
                href_value = anchor_tag['href']
                current_row_values.append(href_value)
        else:
            current_row_values.append(td_tag.getText())
    
    player_stats.append(current_row_values)


stats = pd.DataFrame(player_stats, columns = headers)
stats.rename(columns={"": "Link"}, inplace=True)

# Only keep rookies in fantasy positions
fantasy_positions = ['QB', 'WR', 'TE', 'RB', 'FB']
stats = stats[stats['Pos'].isin(fantasy_positions)]

# Remove all rookies with no college stats
is_string = stats['Link'].apply(lambda x: isinstance(x, str))
starts_with_http = stats['Link'].str.startswith('http', na=False)
stats = stats[is_string & starts_with_http]

# extract_college_career_stats("http://www.sports-reference.com/cfb/players/caleb-williams-3.html")
for index, player_data_row in stats.iterrows():
    college_career_stats = extract_college_career_stats(player_data_row["Link"])
    for column_name, column_val in college_career_stats.items():
        # if column_name not in stats:
        #     stats[column_name] = pd.NA
        stats.loc[index, column_name] = column_val
    
    time.sleep(10)

os.makedirs('data', exist_ok=True)
filepath = os.path.join('data', f"{year}rookiestats.csv")
stats.to_csv(filepath)

print(f"Rookie data for the year {year} has been created.")





