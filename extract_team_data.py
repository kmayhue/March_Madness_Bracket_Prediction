import re
import sys
import pandas as pd
from bs4 import BeautifulSoup

def extract_team_data_from_html_file(filename):
    # Split the filename by the pipe character
    split_filename = filename.split("|")

    # Extract the school name and year from the split filename
    school_name = split_filename[3]
    year = split_filename[4].replace(".html", "")

    # Open the HTML file in read mode
    with open(filename, "r") as f:
        # Read the contents of the file
        html_contents = f.read()

    # Create a Beautiful Soup object from the HTML contents
    soup = BeautifulSoup(html_contents, "html.parser")

    #4. Team stats

    per_game_team_stats = soup.find(id="schools_per_game")
    #convert this html table to a dataframe

    #TODO IMPORTANT: DO NOT USE THE 2008-2009 SEASON, IT IS MISSING KEY STATS
    #TODO IMPORTANT: DO NOT USE THE 2020-2021 SEASON, IT IS MISSING NCAA TOURNAMENT STATS
    # Convert the HTML table into a pandas dataframe
    per_game_team_df = pd.read_html(str(per_game_team_stats))[0]
    #rename the first column to data_type
    per_game_team_df.rename(columns={per_game_team_df.columns[0]: "data_type"}, inplace=True)
    
    #get the team data where data_type == "Team"
    team_averages_df = per_game_team_df[per_game_team_df["data_type"] == "Team"]
    #reset the index
    team_averages_df.reset_index(inplace=True, drop=True)
    #get the opponent data where data_type == "Opponent"
    opponent_averages_df = per_game_team_df[per_game_team_df["data_type"] == "Opponent"]
    #reset the index
    opponent_averages_df.reset_index(inplace=True, drop=True)

    #rename all the columns to opponent_{column_name}
    opponent_averages_df.columns = ["opponent_" + col for col in opponent_averages_df.columns]

    #create a new dataframe that combines the team and opponent dataframes.
    team_data_df = pd.concat([team_averages_df, opponent_averages_df], axis=1)

    #drop the opponent_G column and opponent_MP column
    team_data_df.drop(columns=["opponent_G", "opponent_MP", "data_type", "opponent_data_type"], inplace=True)

    #add the school name and year to the team_data_df dataframe
    team_data_df["school_name"] = school_name
    team_data_df["year"] = year

    #2. coach name and url
    coach_a = soup.find("a", href=re.compile(r"/cbb/coaches/"))
    coach_name = coach_a.text
    coach_url = "www.sports-reference.com" + coach_a["href"]

    #add the coach name and coach url to the team_data_df dataframe
    team_data_df["coach_name"] = coach_name
    team_data_df["coach_url"] = coach_url

    #move the school_name, year, coach_name, and coach_url columns to the front of the dataframe
    cols = team_data_df.columns.tolist()
    cols = cols[-4:] + cols[:-4]
    team_data_df = team_data_df[cols]

    #3. Overall stats of the team

    record_values = []
    psg_values = []
    pag_values = []
    srs_values = []
    sos_values = []

    ps_g_p = soup.find_all("p")
    for elmt in ps_g_p:
        if "Record:" in elmt.text:
            #the record looks like the following:  
            # <strong>Record:</strong> 23-13&nbsp;(10-6, 4th in <a href='/cbb/conferences/mac/2009.html'>MAC</a> East)
            wins = int(elmt.text.split("(")[0].split("-")[0].split(": ")[1])
            losses = int(elmt.text.split("(")[0].split("-")[1])
            conference_record = int(elmt.text.split("(")[1].split(")")[0].split(" in ")[0].split(", ")[1].replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
            conference = elmt.text.split("in ")[1].split(")")[0]

            #add wins, losses, conference record, and conference to the team_data_df dataframe
            team_data_df["wins"] = wins
            team_data_df["losses"] = losses
            team_data_df["conference_record"] = conference_record
            team_data_df["conference"] = conference

        elif "PS/G" in elmt.text:
            ps_g_value = float(elmt.text.split(": ")[1].split(" ")[0])
            ps_g_rank = int(elmt.text.split("(")[1].split(" ")[0].replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
            ps_g_total = int(elmt.text.split("of ")[1].split(")")[0])
            
            #add psg_value, psg_rank, and psg_total to the team_data_df dataframe
            team_data_df["psg_value"] = ps_g_value
            team_data_df["psg_rank"] = ps_g_rank
            team_data_df["psg_total"] = ps_g_total

        elif "PA/G" in elmt.text:
            pa_g_value = float(elmt.text.split(": ")[1].split(" ")[0])
            pa_g_rank = int(elmt.text.split("(")[1].split(" ")[0].replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
            pa_g_total = int(elmt.text.split("of ")[1].split(")")[0])
            
            #add pag_value, pag_rank, and pag_total to the team_data_df dataframe
            team_data_df["pag_value"] = pa_g_value
            team_data_df["pag_rank"] = pa_g_rank
            team_data_df["pag_total"] = pa_g_total

        elif "SRS" in elmt.text:
            srs_value = float(elmt.text.split(": ")[1].split(" ")[0])
            srs_rank = int(elmt.text.split("(")[1].split(" ")[0].replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
            srs_total = int(elmt.text.split("of ")[1].split(")")[0])
            
            #add srs_value, srs_rank, and srs_total to the team_data_df dataframe
            team_data_df["srs_value"] = srs_value
            team_data_df["srs_rank"] = srs_rank
            team_data_df["srs_total"] = srs_total

        elif "SOS" in elmt.text:
            sos_value = float(elmt.text.split(": ")[1].split(" ")[0])
            sos_rank = int(elmt.text.split("(")[1].split(" ")[0].replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
            sos_total = int(elmt.text.split("of ")[1].split(")")[0])
            
            #add sos_value, sos_rank, and sos_total to the team_data_df dataframe
            team_data_df["sos_value"] = sos_value
            team_data_df["sos_rank"] = sos_rank
            team_data_df["sos_total"] = sos_total

    #4. Average height and years of experience of the team, and returning minutes and scoring
    roster_info = soup.find(id="tfooter_roster")
    roster_info_text = roster_info.find("small").text
    
    avg_height_text = roster_info_text.split("Avg. Height:\xa0")[1].split("Avg. Years Exp:\xa0")[0]
    avg_height = int(avg_height_text.split("-")[0]) * 12 + int(avg_height_text.split("-")[1])
    # add avg_height to the team_data_df dataframe
    team_data_df["avg_height"] = avg_height

    avg_years_exp = float(roster_info_text.split("Avg. Years Exp:\xa0")[1].split("Averages weighted by minutes played")[0])
    #add avg_years_exp to the team_data_df dataframe
    team_data_df["avg_years_exp"] = avg_years_exp

    minutes_returned = float(roster_info_text.split("% of minutes played and ")[0][-4:])
    #add minutes_returned to the team_data_df dataframe
    team_data_df["minutes_returned"] = minutes_returned

    scoring_return = float(roster_info_text.split(" of minutes played and ")[1].split("%")[0])
    #add scoring_return to the team_data_df dataframe
    team_data_df["scoring_return"] = scoring_return

    return team_data_df


def main():
    #read the system argument. There will only be a single argument, and it will be a filename
    filename = sys.argv[1]

    team_data = extract_team_data_from_html_file(filename)

if __name__ == '__main__':

    main()