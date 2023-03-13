import random
import pandas as pd


def main():
    #read dataset from "data/formatted/ncaa_regular_season_data.csv"
    ncaa_regular_season_df = pd.read_csv("data/formatted/ncaa_regular_season_data.csv")

    #create a pandas dataframe that will hold the tournament outcomes along with each teams regular season stats
    ncaa_tournament_df = pd.DataFrame()
    #create a list of years from 2010 to 2022 but leave out 2020 (Covid-19 cancelled the season)
    years = [year for year in range(2010, 2023) if year != 2020]
    
    for year in years:
        #create a path to the folder that contains the team data for the current year
        path = f"data/raw/{year}/tournament"
        
        games_df = pd.read_json(f"{path}/games.txt", orient="index")
        print(path)
        #for each row in the games_df dataframe, get the team stats from the ncaa_regular_season_df dataframe
        for index, row in games_df.iterrows():
            #randomly select either 0 or 1. This is to eliminate bias in the dataset. Use built-in random number generator
            random_number = random.randint(0, 1)
            tournament_round = row["round"]
            if random_number == 1:
                team_1_name = row["winner_team_name"]
                team_2_name = row["loser_team_name"]
                team_1_score = row["winner_score"]
                team_2_score = row["loser_score"]
                team_1_win = 1
            else:
                team_1_name = row["loser_team_name"]
                team_2_name = row["winner_team_name"]
                team_1_score = row["loser_score"]
                team_2_score = row["winner_score"]
                team_1_win = 0

            #get the team stats from the ncaa_regular_season_df dataframe
            team_1_stats = ncaa_regular_season_df[(ncaa_regular_season_df["school_name"] == team_1_name) & (ncaa_regular_season_df["year"] == year)]
            #reset the index of the team_1_stats dataframe
            team_1_stats.reset_index(drop=True, inplace=True)
            #rename the columns of the team_1_stats dataframe to team_1_{column_name}
            team_1_stats.rename(columns=lambda x: f"team_1_{x}", inplace=True)
            #get the team stats from the ncaa_regular_season_df dataframe
            team_2_stats = ncaa_regular_season_df[(ncaa_regular_season_df["school_name"] == team_2_name) & (ncaa_regular_season_df["year"] == year)]
            #reset the index of the team_2_stats dataframe
            team_2_stats.reset_index(drop=True, inplace=True)
            #rename the columns of the team_2_stats dataframe to team_2_{column_name}
            team_2_stats.rename(columns=lambda x: f"team_2_{x}", inplace=True)
            #create a pandas dataframe that will hold the team stats for both teams
            team_stats_df = pd.concat([team_1_stats, team_2_stats], axis=1)
            #add the round
            team_stats_df["round"] = tournament_round
            
            #add team_1_win to the team_stats_df dataframe
            team_stats_df["team_1_win"] = team_1_win
            #add the team_1_score to the team_stats_df dataframe
            team_stats_df["team_1_score"] = team_1_score
            #add the team_2_score to the team_stats_df dataframe
            team_stats_df["team_2_score"] = team_2_score

            #add the team_stats_df dataframe to the ncaa_tournament_df dataframe
            ncaa_tournament_df = ncaa_tournament_df.append(team_stats_df, ignore_index=True)
            #reset the index of the ncaa_tournament_df dataframe
            ncaa_tournament_df.reset_index(drop=True, inplace=True)

    #save the ncaa_tournament_df dataframe to a csv file
    #convert team_1_year and team_2_year to integers
    ncaa_tournament_df["team_1_year"] = ncaa_tournament_df["team_1_year"].astype(int)
    ncaa_tournament_df["team_2_year"] = ncaa_tournament_df["team_2_year"].astype(int)
    ncaa_tournament_df.to_csv("data/formatted/ncaa_tournament_all_games.csv", index=False)


    #DONE!
    #There are 3 missing values in the ncaa_tournament_df dataframe. These are the 3 games that were cancelled due to Covid-19
    #These games are all in 2012 and have missing regular season data
    #Filter out team_1_name is Null or team_2_name is Null
    #Filter out minutes_returned	scoring_return = 0 or 1

if __name__ == "__main__":
    main()