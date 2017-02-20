from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
from string import ascii_lowercase

#For store all webpages
webpages = {}
#For store all players info
players= {}
#loop a to z to get all players info (No player name start with x):
for c in range(ord('a'), ord('w')+1)+ range(ord('y'), ord('z')+1):
    # webpages[c]= 'http://www.basketball-reference.com/players/' + chr(c) +"/"
    # print webpages[c]
    #
    webpages[c] = urlopen('http://www.basketball-reference.com/players/' + chr(c) +"/").read()

    soup = BeautifulSoup(webpages[c])
    body = soup.find("table",{"id":"players"}).find("tbody").findAll("tr")

    for element in body:
        players[element.a.get_text()]={}

    prefix = "http://www.basketball-reference.com"

    for element in body:
        #Scrap each individual players' URL link
        players[element.a.get_text()]["link"] = prefix + element.a["href"]

    for element in body:
        #Scrap each individual players' last year
        year_min = element.find('td',{"class":"right", "data-stat":"year_min"}).get_text()
        players[element.a.get_text()]["firstyear"] = year_min

    for element in body:
        #Scrap each individual players' last year
        year_max = element.find('td',{"class":"right", "data-stat":"year_max"}).get_text()
        players[element.a.get_text()]["lastyear"] = year_max

for item in players.keys():
    if int(players[item]["lastyear"])> 2004 & int(players[item]["firstyear"])< 2015:
        print item + ": " + "\n\t" + "link: " + players[item]["link"] + "\n\t" + "last year: " + players[item]["lastyear"]



# out = open('PlayerList.csv','w')
#
#
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
