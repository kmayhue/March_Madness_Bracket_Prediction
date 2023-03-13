import os
import pandas as pd

from extract_team_data import extract_team_data_from_html_file




def main():
    #create a list of years from 2010 to 2022 but leave out 2020 (Covid-19 cancelled the season)
    years = [str(year) for year in range(2010, 2023) if year != 2020]
    
    #for each year in the years list, iterage through each folder that corresponds with the year
    #the folder structure looks like this: data/raw/{year}/teams 

    #create an overall dataframe that will contain all the team data for all years
    overall_ncaa_regular_season_df = pd.DataFrame()

    for year in years:
        #create a path to the folder that contains the team data for the current year
        path = f"data/raw/{year}/teams"
        
        teams_df = pd.read_json(f"{path}/teams.txt", orient="index")

        #get a list of all the files in the folder
        files = os.listdir(path)

        #for each file in the list of files, extract the team data
        for file in files:
            #skip the teams.txt file
            if file == "teams.txt":
                continue
            #create a path to the file
            file_path = f"{path}/{file}"
            print(file_path)
            #extract the team data from the file
            team_data = extract_team_data_from_html_file(file_path)
            #get the official team name from the teams_df dataframe
            team_data["official_team_name"] = teams_df[teams_df["key_team_name"] == team_data["school_name"].values[0]]["official_team_name"].values[0]
            #get the tournament seed from the teams_df dataframe
            team_data["tournament_seed"] = teams_df[teams_df["key_team_name"] == team_data["school_name"].values[0]]["tournament_seed"].values[0]

            #append the team data to the overall dataframe
            overall_ncaa_regular_season_df = overall_ncaa_regular_season_df.append(team_data, ignore_index=True)
            #reset the index of the overall dataframe
            overall_ncaa_regular_season_df.reset_index(drop=True, inplace=True)


    #save the overall dataframe to a csv file
    overall_ncaa_regular_season_df.to_csv("data/formatted/ncaa_regular_season_data.csv", index=False)
            
            




if __name__ == '__main__':
    main()