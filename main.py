# Engineer: Michal Pietruszka, pietruszka@agh.edu.pl
# Date: 03.12.2017

# imports goes here
import os, winshell
import re, sys
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import unicodedata

PATH_LOG =r"C:\Users\HS_MichalP\Documents\Mike_priv\ECG_estimation_repo\EKG_estimation\logs"
# Helper class for printing to the terminal and to log to a file
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
    try:
        PATH_LOG = sys.argv[1]          # Paths where logs will be saved

    except:
        print('Please pass proper directories path in the .bat file')
    print('PATH_LOG = {} \n'.format(PATH_LOG))

    #soup = BeautifulSoup("https://prog.nfz.gov.pl/app-jgp/AnalizaPrzekrojowa.aspx", 'html.parser')
    file_path = r'C:\Users\HS_MichalP\Documents\Mike_priv\ECG_estimation_repo\EKG_estimation\results\results.txt'
    delim = ";"

    with open(file_path, 'w+') as f:
        for i in range(254,771):#164):
            print(i)
            URL = 'https://prog.nfz.gov.pl/app-jgp/AnalizaPrzekrojowaSzczegoly.aspx?id='+str(i)
            soup = BeautifulSoup(urlopen(URL))
            year = 2016 - len(soup.find_all('a')) + 1
            for link in soup.find_all('a'):
                #print(link.get('href'))
                URL_link = link.get('href')
                soup_sub = BeautifulSoup(urlopen(URL_link))
                #print(soup_sub.table) #table.tr)
                a = soup_sub.find_all('table')
                j = 3

                try:
                    kod = a[0].contents[1].contents[1].contents[5].string[0:3]
                    opis_kodu = a[0].contents[1].contents[1].contents[5].string[6:]
                    kod_lb_hospitalizacji = a[1].contents[7].contents[3].string
                    for c in range(0, len(a)):
                        if (a[c].contents[1].contents[1].string =="ICD 9"):
                            #print(c)
                            if (len(a[c].contents)>2):
                                while j <len(a[c].contents):
                                    #print(j)
                                    zabieg_nazwa = a[c].contents[j].contents[3].string
                                    try:
                                        if ("lektrokardiogra" or "EKG") in zabieg_nazwa:
                                            zabieg_lb_hospitalizacji = a[c].contents[j].contents[5].string
                                            #print(zabieg_nazwa)
                                            to_save_str = str(year)+ delim + kod + delim + opis_kodu + delim + str(kod_lb_hospitalizacji)+ \
                                                           delim + zabieg_nazwa + delim + str(zabieg_lb_hospitalizacji)
                                            to_save_str_normal = str(unicodedata.normalize('NFKD', to_save_str).encode('ascii', 'ignore'))
                                            f.write(to_save_str_normal[2:] + '\n')
                                    except:
                                        print("some error in the table field")


                                #print(year, kod, opis_kodu, kod_lb_hospitalizacji, zabieg_nazwa, zabieg_lb_hospitalizacji)
                                    j += 2
                            year +=1
                except:
                    print("Przerwa techniczna")

print('Program finished')

print("bananas")
