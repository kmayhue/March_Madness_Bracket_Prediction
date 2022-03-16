
import sys
import os

from setup import create_folder_structure
from scraper_and_parser_utilities import *

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

def save_tournament_html(download_year, pause=True):
    '''
    This function will do the following:
    
    1. build a url string to the following sports-reference website:
        https://www.sports-reference.com/cbb/postseason/<year>-ncaa.html
    2. check if the url has already been downloaded to our directory.
    3. If already downloaded, then quit the function
    4. If not downloaded, then download from the website and save the html file
    5. Pause for a random amount of time to decrease the website load and avoid detection muahahaha 

    
    '''
    url = "https://www.sports-reference.com/cbb/postseason/{}-ncaa.html".format(str(download_year))
    file_name = url.strip("https://").replace("/", "|")
    #file will be the same as the url minus "https://" and replacing / with |
    save_path = "data/raw/{}/tournament/{}".format(str(download_year), file_name)

    #check if the data is in our directory
    if check_data(file_name, download_year) == False:
        return False
    #save the html to our folder
    if save_html(url, save_path) == False:
        return False
    #pause for a random amount of time
    if pause:
        random_pause()
    

def main():
    '''
    This script has two modes. 1. Download all years since 2009. 2. Download a specific year.
    Specify the year by passing the year after calling this script.

    python download_ncaa_basketball_data.py 2022
    '''
    download_years = determine_years(sys.argv)

    for download_year in download_years:
        #create the folder structure for the current download_year
        folder_structure = {str(download_year): {"tournament": None, "teams": None}}
        create_folder_structure(folder_structure, curr_path="data/raw/")
        #save the tournament html 
        save_tournament_html(download_year, pause=True)


if __name__ == "__main__":
    main()