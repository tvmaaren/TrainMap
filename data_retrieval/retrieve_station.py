#Web Scraping library
from bs4 import BeautifulSoup

import requests

def stationsweb_url(station_name):
    #TODO
    pass

def wikipedia_url(station_name):
    return("https://nl.wikipedia.org/wiki/Station_"+station_name.replace(" ","_"))

class Station:
    def __init__(self,name,coordinates,openings,closures):
        self.name = name
        self.coordinates = coordinates
        self.openings = openings
        self.closures = closures
    def toString(self):
        #TODO
        pass

def retrieve_station(station_name):
    wikipedia_page = requests.get(wikipedia_url(station_name))
    wikipedia_soup = BeautifulSoup(wikipedia_page.text, "html.parser")
    infobox = wikipedia_soup.findAll("table",attrs={"class":"infobox"})
    print(infobox)#Just for testing
retrieve_station("Tricht")#Just for testing
