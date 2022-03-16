from bs4 import BeautifulSoup
import requests
import time
import random

def save_html(url, save_path):
    '''
    This function will grab the html from a website and save it to a file path.
    
    '''
    try:
        resp = requests.get(url)
    except:
        print("Request failed to {}".format(url))
        return False

    try:
        with open(save_path, 'w') as file:
            file.write(resp.text)
    except:
        print("Failed writing html from {} to {}.".format(url, save_path))
        return False
    
    print("Successfully saved html from {} to {}.".format(url, save_path))
    return True

def soup_from_html_file(file_path):
    '''
    This function returns a beautiful soup object from an html file
    '''
    with open(file_path, 'r') as file:
        file_contents = file.read()

    return BeautifulSoup(file_contents, 'html.parser')

def random_pause(max_pause=20):
    '''
    This is definitely not a web crawler because I am randomly pausing....
    '''
    sleep_seconds = random.randint(10, max_pause)
    print("Sleeping for {} seconds.".format(sleep_seconds))
    time.sleep(sleep_seconds)


def main():
    '''
    Examples on how to use the functions above

    file_path = "data/raw/coaches/www.google.com"
    file_soup = soup_from_html_file(file_path)

    print(file_soup.prettify())


    url = "https://www.google.com"
    save_html(url, "data/raw/coaches/{}".format(url.strip("https://")))
    
    '''
    pass


if __name__ == "__main__":
    main()