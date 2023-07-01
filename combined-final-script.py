import requests
from bs4 import BeautifulSoup
import time

requests.packages.urllib3.disable_warnings()


class NdReCrawler:

    def __init__(self):
        self.notifier = False
        self.sids_list = []
        self.data_list = []

    def execute_operation(self):

        """Main driver method for execution"""

        # Collect sids
        self.collect_sids()

        # Scrap datas using sids
        self.scrap_data()

    def collect_sids(self):

        """Collects sids by crawling over NDRE website and crawls until it reaches the end"""

        # Loop terminator
        is_end = True

        # Paginator
        page = 1

        print('Collecting SIDS . . . ')  # Remove this line

        # Main loop
        while is_end:

            # Get data
            data = self.request_data('https://ndre.sreda.gov.bd/index.php?id=1&i=0&pg=', page)

            # Get the required table
            table = data.find_all('table')[0]

            # Collect all table rows
            all_rows = table.find_all('tr')
            rows = all_rows[3:]
            sids = []

            # Loop over rows
            for r in rows:

                # Only collect sids from the row
                column = r.find_all('td')[2]
                sids.append(column.text.strip())

            # If there's no sids terminate the loop in next iteration
            if len(sids) == 0:
                is_end = False

            # Else append sids to the main sids_list for scrapping and increase the paginator by one
            else:
                print(sids)  # Remove this one line
                self.sids_list.extend(sids)
                page += 1

        # Remove these lines
        print('Collecting SIDS completed')
        print()

    def scrap_data(self):

        """Scraps data from webpage by using sids collected previously, and stores them in a dictionary.
            We can use the dictionary to use these collected data anywhere we want.

            NOTE :
                When we scrap over the page, the page has only one root table, which is than divided into sub tables,
                like a nested list. So it was bit tricky to figure out how to get the exact table data.
                That's why there's a nasty table calls and row calls over the table only for collecting valid and
                accurate data.
            """

        # Looping over sids list
        for sids in self.sids_list:

            # Get data
            data = self.request_data('https://ndre.sreda.gov.bd/index.php?id=06&kid=', sids)

            dic = {}
            # Getting all tables
            table = data.find_all('table')

            # Getting first table rows, which is sub first table of root table
            rows = table[0].find_all('tr')[0].find_all('table')[0]

            # Finding all rows
            row = rows.find_all('tr')

            # Looping over all rows
            for r in row[1:]:

                # Getting columns
                col = r.find_all('td')

                # Adding columns to the tmp dictionary
                dic[col[0].text.strip()] = col[2].text.strip()

            # Getting second table rows, which is sub second table of the root table
            rows1 = table[0].find_all('tr')[0].find_all('table')[1]

            # Finding all rows init
            row1 = rows1.find_all('tr')

            # Looping over all rows
            for r in row1[1:]:

                # Getting all columns
                col = r.find_all('td')

                # Adding columns to the tmp dictionary
                dic[col[0].text.strip()] = col[2].text.strip()

            # Remove these lines in case of real use, these are just to show the output
            for k, v in dic.items():
                print(k, ' : ', v)

            print()
            print('-------------')
            print()

            # Appending to the final list
            self.data_list.append(dic)

    def request_data(self, url, arg):

        """Sends requests to given url with argument and gets html data in text format, then returns
            it as BS4 datatype for further operation"""

        self.notifier = True  # Only for ignoring annoying style guide

        # Getting html response, converting that to text and converting to BS4 data type and returning it.
        html_data = requests.get(f'{url}{arg}', verify=False).text

        return BeautifulSoup(html_data, 'html.parser')

    def peak_data(self):

        """Only for peaking data"""

        for data in self.data_list:
            print(data)


def crawl():

    obj = NdReCrawler()
    obj.execute_operation()


crawl()
