import requests
from bs4 import BeautifulSoup
import time

requests.packages.urllib3.disable_warnings()


html_data = requests.get('https://ndre.sreda.gov.bd/index.php?id=06&kid={sid goes here}', verify=False)

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
