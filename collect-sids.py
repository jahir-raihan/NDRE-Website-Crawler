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
        sids_list.extend(sids)
        page += 1


"""Collects SIDS for further scrapping"""
