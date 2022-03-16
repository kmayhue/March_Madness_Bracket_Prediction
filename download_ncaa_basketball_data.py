
import sys
import os
import requests
import time
from setup import create_folder_structure

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def determine_years(sys_args):
    if len(sys_args) == 1:
        return [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    elif len(sys_args) == 2 and is_integer(sys_args[1]):
        return [int(sys_args[1])]

def check_data(filename, download_year):
    '''
    To avoid re-downloading existing data, we will check if the data already exists in a folder.
    If it does, warn the user and exit.
    '''
    #TODO a better implementation would be able to iterate arbitrarily through the folder structure, but
    #for now, I will hardcode the 3 paths (teams, coaches, and tournament).

    check_folders = ["data/raw/{}/tournament/".format(str(download_year)), "data/raw/{}/teams/".format(str(download_year)), "data/raw/coaches/"]

    for check_path in check_folders:
        file_path = "{}{}".format(check_path, filename)
        if os.path.isfile(file_path):
            print("{} has already been downloaded to {}. If you need to re-download the data, delete this file and re-run this script.".format(filename, file_path))
            return False
    print("Data has not been downloaded. This program will now attempt to download {}.".format(filename))
    return True

def get_tournament_html(year):
    '''
    This function will hit the sportsreference website and grab the tournament information 
    for a given year. Then, it will save that html file to the following folder:

        data
            -raw
                -year
                    -tournament
                        -https://www.sports-reference.com/cbb/postseason/<year>-ncaa.html

    This assumes that you have already run setup.py
    '''
    pass

def random_pause():
    '''
    This is definitely not a web crawler because I am randomly pausing....
    '''
    pass

def main():
    '''
    This script has two modes. 1. Download all years since 2009. 2. Download a specific year.
    Specify the year by passing the year after calling this script.

    python download_ncaa_basketball_data.py 2022
    '''
    download_years = determine_years(sys.argv)

    for download_year in download_years:
        check_data("text.txt", download_year)

        folder_structure = {str(download_year): {"tournament": None, "teams": None}}
        create_folder_structure(folder_structure, curr_path="data/raw/")

if __name__ == "__main__":
    main()