import datetime
import os

import requests
from bs4 import BeautifulSoup as bs

# Create output directory if it does not exist yet.
try:
    os.mkdir('OUTPUT')
except FileExistsError:
    pass

# This scripts starts at gruusbek.nl and goes trough every folder from start_year till the current year.
URL = 'https://gruusbek.nl/schlagers-'
old_schlagers = 'oud'
start_year = 1988
current_year = datetime.date.today().year

# Create an arraylist with all the URLs of the pages where slagers are.
ALLURLS = [URL + old_schlagers]
for i in range(start_year, current_year + 1):
    ALLURLS.append(URL + str(i))

# IDK copied from tutorial. Does the requests to a url and returns all of the html i think.
def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')

# This loops trough all the urls of all the schlager pages.
for yearURL in ALLURLS:

    # Creates a folder within the output folder containing where the schlagers will be sorted in by year.
    try:
        os.mkdir('OUTPUT/' + yearURL[20:])
    except FileExistsError:
        pass

    # This loops trough every a element on the page of a specific year
    for link in get_soup(yearURL).find_all('a'):
        # Check for a elements with a href and save it
        href_link = link.get('href')

        # If the href containts a .mp3 file, save it in the output folder sorted by year.
        if '.mp3' in href_link:
            with open('OUTPUT/' + yearURL[20:] + '/' + href_link.rsplit('/', 1)[1], 'wb') as file:
                response = requests.get(href_link)
                file.write(response.content)
