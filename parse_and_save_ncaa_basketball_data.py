from setup import *
from scraper_and_parser_utilities import *
import json



def parse_tournament_data(file_path, download_year):
    '''
    This function does the following:
    
    1. get a soup object from an html file containing NCAA tournament information.
    2. Parse the tournament data to get the games for the given NCAA tournament 
    3. Save this game information
    '''
    file_soup = soup_from_html_file(file_path)

    '''
    The div is structured in the following way:
    -brackets
        -bracket 
            -east
                -round 1
                    -div
                        -div 1 (Winner)
                            -div 1
                                -get href to team
                                -get team id from href 
                                -get nicely formatted team name
                            -div 2 
                                -get winning score
                        -div 2 (loser)
                -round 2
                -round 3
                -round 4
        -bracket
            -west
        -bracket
            -midwest
        -bracket
            -south
        -bracket
            -national
    
    '''
    #json to keep track of all the tournament games
    games_json = {}
    #arbitrary id for dataframe purposes
    games_id = 0

    #json to get all team_urls
    teams_json = {}

    regions = ["east", "west", "midwest", "south", "national"]

    for region in regions:
        for region_set in file_soup.find_all("div", {"id": region}):
            #due to the way that the html is set up, the final 4 is at the same 'level' as
            #the previous rounds. The final 4 is technically the 5th round.
            if region == "national":
                round_counter = 5
            else:
                round_counter = 1
            for round in region_set.find_all("div", {"class": "round"}):
                for game in round.find_all("div", recursive=False):
                    game_divs = game.find_all("div")
                    #the winner is the first div
                    winner_div = game_divs[0]
                    #the loser is the second div
                    loser_div = game_divs[1]
                    #determine seeding
                    winner_seed = game_divs[0].span.contents[0]
                    loser_seed = game_divs[1].span.contents[0]
                    #team name, score, and url are in the links within this div
                    winner_links = game_divs[0].find_all("a")
                    loser_links = game_divs[1].find_all("a")
                    #url to download team stats
                    winner_team_url = winner_links[0]["href"]
                    loser_team_url = loser_links[0]["href"]
                    #offical team_name (i.e. Michigan or Arizona)
                    winner_official_team_name = winner_links[0].contents[0]
                    loser_official_team_name = loser_links[0].contents[0]
                    #the team name that will serve as the team "key"
                    winner_key_team_name = winner_links[0]["href"].split("/")[3]
                    loser_key_team_name = loser_links[0]["href"].split("/")[3]
                    #the score for the game
                    winner_team_score = winner_links[1].contents[0]
                    loser_team_score = loser_links[1].contents[0]

                    #save the data in the respective data structure
                    games_json[str(games_id)] = {"year": download_year, \
                                "round": round_counter, \
                                "winner_team_name": winner_key_team_name, \
                                "loser_team_name": loser_key_team_name, \
                                "winner_score": winner_team_score, \
                                "loser_score": loser_team_score}
                    #add 1 to the games_id
                    games_id += 1
                    #populate the teams_json with the winner and loser team data
                    teams_json[winner_team_url] = { \
                                "key_team_name": winner_key_team_name, \
                                "official_team_name": winner_official_team_name, \
                                "year": download_year, \
                                "tournament_seed": winner_seed}
                    teams_json[loser_team_url] = { \
                                "key_team_name": loser_key_team_name, \
                                "official_team_name": loser_official_team_name, \
                                "year": download_year, \
                                "tournament_seed": loser_seed}

                    

                round_counter += 1

                if round_counter == 5 and region != "national":
                    break
                elif round_counter == 7 and region == "national":
                    break

    return {"tournament_data": games_json, "team_data": teams_json}
    

def save_dict_to_file(data, file_path):
    json_string = json.dumps(data)
    with open(file_path, 'w') as outfile:
        outfile.write(json_string)

def load_dict_from_file(file_path):
    with open(file_path, 'r') as infile:
        read_file = infile.read()
    return json.loads(read_file)


def main():

    teams_json = {}
    download_years = determine_years(sys.argv)
    for download_year in download_years:
        print("Parsing data from the year {}".format(str(download_year)))
        #parse the tournament data
        file_path = "data/raw/{}/tournament/www.sports-reference.com|cbb|postseason|{}-ncaa.html".format(str(download_year), str(download_year))
        tournament_jsons = parse_tournament_data(file_path, download_year)

        tournament_file_path = "data/raw/{}/tournament/games.txt".format(str(download_year))
        team_file_path = "data/raw/{}/teams/teams.txt".format(str(download_year))

        save_dict_to_file(tournament_jsons["tournament_data"], tournament_file_path)
        save_dict_to_file(tournament_jsons["team_data"], team_file_path)
        
    



if __name__ == "__main__":
    main()