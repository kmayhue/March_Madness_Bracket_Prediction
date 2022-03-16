import os 
import sys

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def determine_years(sys_args):
    if len(sys_args) == 1:
        return [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022]
    elif len(sys_args) == 2 and is_integer(sys_args[1]):
        return [int(sys_args[1])]

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
    folder_structure = {"data": {"raw": {"coaches": None}, "formatted": None}}
    create_folder_structure(folder_structure)

    #TODO automatically download python3 and pip
    #TODO automatically download venv (would need a shell script) pip install venv
    #TODO automatically activate venv (shell script)  source .venv/bin/activate
    #TODO automatically create a requirements.txt file vi requirements.txt
    #TODO automatically pip the requirements.txt file  python -m pip install -r requirements.txt



if __name__ == "__main__":
    main()