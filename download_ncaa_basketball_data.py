
from setup import *
from scraper_and_parser_utilities import *
from parse_and_save_ncaa_basketball_data import *

import pandas as pd

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

def load_all_teams_from_html(download_year):
    '''
    This function takes a download_year and returns the json with all the team data.
    '''

    return load_dict_from_file("data/raw/{}/teams/{}".format(str(download_year), "teams.txt"))

def save_team_html(download_year, team_url, pause=True):
    '''
    This function will do the following:
    
    1. build a url string to the following sports-reference website:
        https://www.sports-reference.com/cbb/schools/<team>/<year>.html"
    2. check if the url has already been downloaded to our directory.
    3. If already downloaded, then quit the function
    4. If not downloaded, then download from the website and save the html file
    5. Pause for a random amount of time to decrease the website load and avoid detection muahahaha 

    
    '''
    url = "https://www.sports-reference.com{}".format(team_url)
    file_name = url.strip("https://").replace("/", "|")
    
    #file will be the same as the url minus "https://" and replacing / with |
    save_path = "data/raw/{}/teams/{}".format(str(download_year), file_name)

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
    teams_json = {}
    for download_year in download_years:
        #create the folder structure for the current download_year
        folder_structure = {str(download_year): {"tournament": None, "teams": None}}
        create_folder_structure(folder_structure, curr_path="data/raw/")
        
        #save the tournament html 
        save_tournament_html(download_year, pause=True)

        print("Parsing data from the year {}".format(str(download_year)))
        #parse the tournament data
        file_path = "data/raw/{}/tournament/www.sports-reference.com|cbb|postseason|{}-ncaa.html".format(str(download_year), str(download_year))
        tournament_jsons = parse_tournament_data(file_path, download_year)

        tournament_file_path = "data/raw/{}/tournament/games.txt".format(str(download_year))
        team_file_path = "data/raw/{}/teams/teams.txt".format(str(download_year))

        save_dict_to_file(tournament_jsons["tournament_data"], tournament_file_path)
        save_dict_to_file(tournament_jsons["team_data"], team_file_path)

        #try to download team_data
        #TODO this is how to convert the json to a dictionary
        #teams_df = pd.DataFrame.from_dict(load_all_teams_from_html(download_year), orient="index")
        teams_dict = load_all_teams_from_html(download_year)
        #LET THE SCRAPING BEGIN!
        for team_url in teams_dict.keys():
            save_team_html(download_year, team_url, pause=True)

if __name__ == "__main__":
    main()