# Engineer: Michal Pietruszka, pietruszka@agh.edu.pl
# Date: 03.12.2017

# imports goes here
import os, winshell
import re, sys
import time



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
    sys.stdout = Logger()
    try:
        PATH_LOG = sys.argv[1]          # Paths where logs will be saved
    except:
        print('Please pass proper directories path in the .bat file')

    print('PATH_LOG = {} \n'.format(PATH_LOG))



print('Program finished')
