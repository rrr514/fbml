from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import time

def extract_college_career_stats(url):
    if not url or not isinstance(url, str) or not url.startswith('http'):
        print(f"Invalid or missing URL: {url}")
        return {}
    
    print(f"Fetching college data from: {url}")
    college_career_stats = {}
    html = urlopen(url)
    soup = BeautifulSoup(html, features="lxml")

    # Extract passing stats
    passing_table = soup.find('table', id='passing_standard')
    if not passing_table:
        print(f"Could not find passing_standard table at {url}")
        return college_career_stats
    
    tfoot = passing_table.find('tfoot')
    if not tfoot:
        print(f"Could not find tfoot in passing_standard table at {url}")
        return college_career_stats
    
    career_row = None
    career_row_id = f"{passing_table.get('id', 'passing_standard')}.Career"
    career_row = tfoot.find('tr', id=career_row_id)

    if not career_row:
        print("Manual search for passing career row")
        for row_in_footer in tfoot.find_all('tr'):
            first_header_cell = row_in_footer.find('th')
            if first_header_cell and 'Career' in first_header_cell.get_text(strip=True):
                career_row = row_in_footer
                break
    
    if not career_row:
        print(f"Could not find passing_table Career row in table footer at {url}")
        return college_career_stats
    
    # Extract all data-stat attributes from the passing career row
    for cell in career_row.find_all(['th', 'td']):
        if cell.has_attr('data-stat'):
            stat_label = cell['data-stat']
            stat_value = cell.get_text(strip = True)
            column_name = f"Coll_{stat_label}"
            college_career_stats[column_name] = stat_value

    # Extract rushing/recieving stats
    rush_receive_table = soup.find('table', id='rushing_standard')
    if not rush_receive_table:
        print(f"Could not find rush/recieve table at {url}")
        return college_career_stats
    
    tfoot = rush_receive_table.find('tfoot')
    if not tfoot:
        print(f"Could not find tfoot in rush/recieve table at {url}")
        return college_career_stats
    
    career_row = None
    career_row_id = f"{rush_receive_table.get('id', 'rushing_standard')}.Career"
    career_row = tfoot.find('tr', id=career_row_id)

    if not career_row:
        print("Manual search for rush/receive career row")
        for row_in_footer in tfoot.find_all('tr'):
            first_header_cell = row_in_footer.find('th')
            if first_header_cell and 'Career' in first_header_cell.get_text(strip=True):
                career_row = row_in_footer
                break

    if not career_row:
        print(f"Could not find rush/receieve career row in {url}")
        return college_career_stats
    
    # Extract all data_stat attributes from the rush/receive career row
    for cell in career_row.find_all(['th', 'td']):
        if cell.has_attr('data-stat'):
            stat_label = cell['data-stat']
            stat_value = cell.get_text(strip=True)
            column_name = f"Coll_{stat_label}"
            college_career_stats[column_name] = stat_value

    print(f"Extracted from passing career row: {college_career_stats}")
     
    return college_career_stats



parser = argparse.ArgumentParser(description="Preprocess rookie stats by year")
parser.add_argument("year", type=int, help="Season year to process")

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
        if column_name not in stats:
            stats[column_name] = pd.NA
        stats[index, column_name] = column_val
    
    time.sleep(10)

stats.to_csv(f"{year}rookiestats.csv")

print(f"Rookie data for the year {year} has been created.")





