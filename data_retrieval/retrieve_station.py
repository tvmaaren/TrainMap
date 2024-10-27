#Web Scraping library
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

import requests

def stationsweb_url(station_name):
    return("https://www.stationsweb.nl/station.asp?station="+station_name.lower())

def wikipedia_url(station_name):
    return("https://nl.wikipedia.org/wiki/Station_"+station_name.replace(" ","_"))

#For example: This converts 52° 14′ 17″ to 52.238056
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
        

def retrieve_station(station_name):
    stationsweb_page = requests.get(stationsweb_url(station_name))
    stationsweb_soup = BeautifulSoup(stationsweb_page.text, "html.parser")
    tables = stationsweb_soup.findAll("table")
    openings_and_closures = tables[4]
    openings_and_closures_list = openings_and_closures.findAll("tr")
    
    opening_dates = []
    closure_dates = []
    for opening_or_closure in openings_and_closures_list:
        opening_and_closure_columns = opening_or_closure.findAll("td")
        is_opening_or_closure = opening_and_closure_columns[0].text
        date = opening_and_closure_columns[1].text
        if(is_opening_or_closure=="Geopend op" or is_opening_or_closure == "Heropend op"):
            opening_dates.append(date)
        if(is_opening_or_closure=="Gesloten op"):
            closure_dates.append(date)

    #For the coordinates I need to load wikipedia, because stationsweb does not
    #provide them.
    wikipedia_page = requests.get(wikipedia_url(station_name))
    wikipedia_soup = BeautifulSoup(wikipedia_page.text, "html.parser")
    wikipedia_coordinates = wikipedia_soup.find("span", attrs={"id":"tpl_Coordinaten"})
    [latitude_string, longitude_string] = wikipedia_coordinates.a.text.split(", ")
    latitude = string_to_coordinates(latitude_string[:-3])
    longitude = string_to_coordinates(longitude_string[:-3])
    
    station = Station(station_name,(latitude,longitude),opening_dates,closure_dates)
    return(station)
root = retrieve_station("Twello").toXML()#Just for testing
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)
tree.write("treey")
