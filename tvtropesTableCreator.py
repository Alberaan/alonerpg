#py
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

def createFile(title, contents):
    fichero = title + ".txt"
    print("Escribiendo en " + fichero)
    with open(fichero, "w", encoding="utf-8") as fileToWrite:
        fileToWrite.write(contents)
    print("Terminado")

def fixTitle(title):
    titleToReturn = ""
    for i in title:
        if i.isalnum() or i == " ":
            titleToReturn += i
        else:
            titleToReturn += "_"

    return titleToReturn

def getTropes(url):
    tvtropes_link = url
    url ='http://dbtropes.org/info?uri=' + tvtropes_link + "&submit=Reverse+URI+Lookup"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    unfilteredTitle = soup.select("head title")[0].get_text().replace(" - DBTropes","")
    title = fixTitle(unfilteredTitle)
    
    tropes = soup.select("tr.bg1 a")

    text = ""

    for trope in tropes:
        if "Main" in trope["href"]:
            toAdd = trope.get_text().split("/")[0]

            if any(char.isalnum() for char in toAdd): 
                text += toAdd + "\n"

    return title, text[:-1] # I remove the last carriage return of the text

def main():
    if (sys.argv[1] == "-i"):
        while(1):
            url = input("Introduce la url de tvtropes.org a partir de la cual quieras crear una tabla aleatoria:\n")
            title, text = getTropes(url)
            print("Tabla para: " + title + "\n")
            print(text)
    
    else:
        title, text = getTropes(sys.argv[1])
        createFile(title, text)

if __name__ == main():
    main()
