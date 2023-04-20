import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a request to the URL
url = "https://en.wikipedia.org/wiki/ATP_rankings"
response = requests.get(url)

# Parse HTML content with Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find the ATP rankings table
table = soup.find("table", {"class": "wikitable nowrap"})

# Extract the table headers and rows
headers = []
rows = []
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)
    else:
        header_cells = row.find_all("th")
        headers = [cell.text.strip() for cell in header_cells]
# Create a DataFrame from the scraped data
df = pd.DataFrame(rows, columns=headers)

# Print the DataFrame
print(df)
# replace columns with only spaces with zeros
df.loc[:, df.eq(' ').all()] = 0
df = df.replace("", 0)
df[['Name','Country']] = df.Player.str.split('\(|\)', expand=True).iloc[:,[0,1]]
df=df.drop(columns=['Player'])
df = df.reindex(columns=['No.','Name','Country','Points','Move'])
df.to_csv('Atp_Clean.csv', index=False)