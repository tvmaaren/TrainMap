ittps://www.stationsweb.nl/station.asp?station=ijmuidenhan on wikipedia.
iWeb Scraping library
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

iWeb Scraping library
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

#This dictionary is used to translate between the two
stationsweb_to_wikipedia = {"Voorst- Empe":"Voorst-Empe"}

import requests

def wikipedia_url(station_name):
    return("https://nl.wikipedia.org/wiki/Station_"+station_name.replace(" ","_"))

def string_to_coordinates(string):
    string_without_symbols = string.replace("°","").replace("′","").replace("″","")
    [number_1,number_2,number_3] = string_without_symbols.split()
    return(int(number_1)+(int(number_2)/60)+(int(number_3)/3600))
    

class Station:
    def __init__(self,name,coordinates,openings,closures):
        self.name = name
        self.coordinates = coordinates
        self.openings = openings
        self.closures = closures
    def toXML(self):
        root = ET.Element("Station")

        ET.SubElement(root, "Name").text = self.name

        coordinates = ET.SubElement(root,"Coordinates")
        
        (latitude,longitude) = self.coordinates
        ET.SubElement(coordinates, "Latitude").text = str(latitude)
        ET.SubElement(coordinates, "Longitude").text = str(longitude)
        
        openings = ET.SubElement(root,"Openings")
        for opening in self.openings:
            ET.SubElement(openings, "Opening").text = opening
        
        closures = ET.SubElement(root,"closures")
        for closure in self.closures:
            ET.SubElement(closures, "Closure").text = closure

        return(root)
        

def retrieve_station(stationsweb_url):
    stationsweb_page = requests.get(stationsweb_url)
    stationsweb_soup = BeautifulSoup(stationsweb_page.text, "html.parser")

    station_name = stationsweb_soup.find("h3").text[8:-1]

    tables = stationsweb_soup.findAll("table")
    openings_and_closures = tables[4]
    openings_and_closures_list = openings_and_closures.findAll("tr")
    
    opening_dates = []
    closure_dates = []
    for opening_or_closure in openings_and_closures_list:
        opening_and_closure_columns = opening_or_closure.findAll("td")
        is_opening_or_closure = opening_and_closure_columns[0].text
        date = opening_and_closure_columns[1].text
        if(is_opening_or_closure[:7]=="Geopend" or is_opening_or_closure[:8]=="Heropend"):
            opening_dates.append(date)
        elif(is_opening_or_closure[:8]=="Gesloten"):
            closure_dates.append(date)

    #For the coordinates I need to load wikipedia, because stationsweb does not
    #provide them.
    latitude = None
    longitude = None
    try:
        wikipedia_station_name = ""
        if(station_name in stationsweb_to_wikipedia.keys()):
            wikipedia_station_name = stationsweb_to_wikipedia[station_name]
        else:
            wikipedia_station_name = station_name
        wikipedia_page = requests.get(wikipedia_url(wikipedia_station_name))
        wikipedia_soup = BeautifulSoup(wikipedia_page.text, "html.parser")
        wikipedia_coordinates = wikipedia_soup.find("span", attrs={"id":"tpl_Coordinaten"})
        [latitude_string, longitude_string] = wikipedia_coordinates.a.text.split(", ")
        latitude = string_to_coordinates(latitude_string[:-3])
        longitude = string_to_coordinates(longitude_string[:-3])
    except:
        print(f"Was not able to retrieve the coordinates of station {station_name}")
    
    station = Station(station_name,(latitude,longitude),opening_dates,closure_dates)
    return(station)
