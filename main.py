# Engineer: Michal Pietruszka, pietruszka@agh.edu.pl
# Date: 03.12.2017

# imports goes here
import sys
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import unicodedata

PATH_LOG =r"your_path_to_logs\EKG_estimation\logs"

# Helper class for printing to the terminal and to log to a file for debugging purposes
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.log = open(PATH_LOG + "/log_" + timestr + ".dat", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

if __name__ == "__main__":
    #sys.stdout = Logger()
    # Read variables from .bat script
    try:
        PATH_LOG = sys.argv[1]          # Paths where logs will be saved
    except:
        print('Please pass proper directories path in the .bat file')
    print('PATH_LOG = {} \n'.format(PATH_LOG))

    file_path = r'C:\Users\HS_MichalP\Documents\Mike_priv\ECG_estimation_repo\EKG_estimation\results\results.txt'
    delim = ";"

    with open(file_path, 'w+') as f:
        # Run loop for every id that is on the NFZ webpage
        for id in range(1, 771):
            print(id)
            # Main page to be scraped
            URL = 'https://prog.nfz.gov.pl/app-jgp/AnalizaPrzekrojowaSzczegoly.aspx?id='+str(id)
            soup = BeautifulSoup(urlopen(URL))

            # open every link in a sub-page
            for link in soup.find_all('a'):
                URL_link = link.get('href')
                soup_sub = BeautifulSoup(urlopen(URL_link))
                # Find all tables
                a = soup_sub.find_all('table')
                j = 3
                # If there is any data in the result web page, proceed
                try:
                    # Extract data from tables
                    year = a[0].contents[1].contents[1].contents[1].string[5:]
                    code = a[0].contents[1].contents[1].contents[5].string[0:3]
                    code_description = a[0].contents[1].contents[1].contents[5].string[6:]
                    hospitalization_count = a[1].contents[7].contents[3].string
                    # look for the table that list ICD 9 procedure codes
                    for c in range(0, len(a)):
                        if (a[c].contents[1].contents[1].string =="ICD 9"):
                            # check if this table isn't empty
                            if (len(a[c].contents) > 2):
                                # Look for a specific substring in the procedure's name column
                                while j <len(a[c].contents):
                                    procedure_name = a[c].contents[j].contents[3].string
                                    try:
                                        if ("lektrokardiogra" or "EKG") in procedure_name:
                                            procedure_performed_count = a[c].contents[j].contents[5].string
                                            # All data are gathered, convert them to string
                                            to_save_str = str(year)+ delim + code + delim + code_description + delim + str(hospitalization_count)+ \
                                                           delim + procedure_name + delim + str(procedure_performed_count)
                                            # Normalize data from unicode to ASCII code
                                            to_save_str_normal = str(unicodedata.normalize('NFKD', to_save_str).encode('ascii', 'ignore'))
                                            # Save line with data to the file
                                            f.write(to_save_str_normal[2:] + '\n')
                                    except:
                                        # Catch error from table scraping
                                        print("Error in the table field")
                                    # increment row counter to the next row
                                    j += 2
                except:
                    # catch error when webpage is empty
                    print("Przerwa techniczna")

print('Program finished')
