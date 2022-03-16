"""



The purpose of this script is to download the NCAA March Madness Data from the Sports Reference website.



Folder structure

-data
    -raw
        -year
            -tournament
                -https://www.sports-reference.com/cbb/postseason/<year>-ncaa.html
            -teams
                -https://www.sports-reference.com/cbb/schools/baylor/2021.html
        -coaches
            -https://www.sports-reference.com/cbb/coaches/juwan-howard-1.html
            -https://www.sports-reference.com/cbb/coaches/scott-drew-1.html
            -etc..
    -formatted
        -march_madness_dimensions.csv

"""
import os 




def create_folder_structure(folder_structure, curr_path=""):
    '''
    This function recursively creates folders given a nested dictionary to define the folder structure.
    '''
    for key in folder_structure.keys():
        if folder_structure[key] == None:
            if not os.path.exists("{}{}".format(curr_path,key)):
                os.makedirs("{}{}".format(curr_path,key))
        else:
            if not os.path.exists("{}{}".format(curr_path,key)):
                os.makedirs("{}{}".format(curr_path,key))
            create_folder_structure(folder_structure[key], "{}{}/".format(curr_path, key))









def main():
    '''
    Create the following structure

    -data
        -raw
            -year
                -tournament
                    -https://www.sports-reference.com/cbb/postseason/<year>-ncaa.html
                -teams
                    -https://www.sports-reference.com/cbb/schools/baylor/2021.html
            -coaches
                -https://www.sports-reference.com/cbb/coaches/juwan-howard-1.html
                -https://www.sports-reference.com/cbb/coaches/scott-drew-1.html
                -etc..
        -formatted
    '''
    folder_structure = {"data": {"raw": {"year": {"tournament": None, "teams": None}, "coaches": None}, "formatted": None}}
    create_folder_structure(folder_structure)

    #TODO automatically download python3 and pip
    #TODO automatically download venv (would need a shell script) pip install venv
    #TODO automatically activate venv (shell script)  source .venv/bin/activate
    #TODO automatically create a requirements.txt file vi requirements.txt
    #TODO automatically pip the requirements.txt file  python -m pip install -r requirements.txt



if __name__ == "__main__":
    main()