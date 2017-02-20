from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import html5lib
from string import ascii_lowercase

#website prefix
prefix = "http://www.basketball-reference.com"
#For store all webpages
webpages = {}
#For store all players info
players= {}
#loop a to z to get all players info (No player name start with x):
for c in range(ord('a'), ord('w')+1)+ range(ord('y'), ord('z')+1):
    webpages[c] = urlopen('http://www.basketball-reference.com/players/' + chr(c) +"/").read()

    soup = BeautifulSoup(webpages[c],'html5lib')
    #find the player tables
    body = soup.find("table",{"id":"players"}).find("tbody").findAll("tr")

    for element in body:

        players[element.a.get_text()]={}

        #Scrap each individual players' first year
        name = element.find('th',{"class":"left", "data-stat":"player"}).a.get_text()
        players[element.a.get_text()]["name"] = name

        #Scrap each individual players' URL link
        players[element.a.get_text()]["link"] = prefix + element.a["href"]

        #Scrap each individual players' first year
        year_min = element.find('td',{"class":"right", "data-stat":"year_min"}).get_text()
        players[element.a.get_text()]["firstyear"] = year_min

        #Scrap each individual players' last year
        year_max = element.find('td',{"class":"right", "data-stat":"year_max"}).get_text()
        players[element.a.get_text()]["lastyear"] = year_max

        #Scrap each individual players' position
        pos = element.find('td',{"class":"center ","data-stat":"pos"}).get_text()
        players[element.a.get_text()]["position"] = pos

        #Scrap each individual players' height
        height = element.find('td',{"class":"right ", "data-stat":"height"}).get_text()
        players[element.a.get_text()]["height"] = height

        #Scrap each individual players' weight
        weight = element.find('td',{"class":"right ", "data-stat":"weight"}).get_text()
        players[element.a.get_text()]["weight"] = weight

        #Scrap each individual players' colleage name
        try:
            college = element.find('td',{"class":"left ", "data-stat":"college_name"}).a.get_text()
        except AttributeError:
            players[element.a.get_text()]["college"] = ''
            continue #skip to the next loop.
        else:
            players[element.a.get_text()]["college"] = college


for item in players.keys():
    if int(players[item]["lastyear"])> 2004 & int(players[item]["firstyear"])< 2015:
        print players[item]["name"] + ": " + "\n\t" + "link: " + players[item]["link"] + "\n\t" + "last year: " + players[item]["lastyear"] + "\n\t" + "college: " + players[item]["college"]



# out = open('PlayerList.csv','w')
# #print header
# for j in header.find_all("th"):
# 	out.write(j.get_text()+",")
# out.write("\n")
#
# # print table
# for i in table:
#     d=i.find("th");out.write(d.get_text()+",")
#     for j in i.find_all("td"):
#         out.write(j.get_text()+",")
#     out.write("\n")
#
# out.close()
# print 'Done!'
#retrieve teams with detailed profiles
