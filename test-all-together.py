import requests
from bs4 import BeautifulSoup
import time

requests.packages.urllib3.disable_warnings()

sids_list = []
is_end = True
page = 1
while is_end:
    html_data = requests.get(f'https://ndre.sreda.gov.bd/index.php?id=1&i=0&pg={page}', verify=False)

    data = BeautifulSoup(html_data.text, 'html.parser')
    table = data.find_all('table')[0]

    all_rows = table.find_all('tr')
    rows = all_rows[3:]
    sids = []
    for r in rows:
        column = r.find_all('td')[2]
        sids.append(column.text.strip())
    if len(sids) == 0:
        is_end = False
    else:
        print(sids)
        sids_list.extend(sids)
        page += 1


# Let's scrap the pages using sids


html_data = requests.get('https://ndre.sreda.gov.bd/index.php?id=06&kid=5419', verify=False)

data = BeautifulSoup(html_data.text, 'html.parser')
table = data.find_all('table')

rows = table[0].find_all('tr')[0].find_all('table')[0]

row = rows.find_all('tr')

for r in row[1:]:
    col = r.find_all('td')
    print(col[0].text, ' : ', col[2].text)


rows1 = table[0].find_all('tr')[0].find_all('table')[1]

row1 = rows1.find_all('tr')

for r in row1[1:]:
    col = r.find_all('td')
    print(col[0].text, ' : ', col[2].text)
