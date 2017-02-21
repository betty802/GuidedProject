from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import html5lib
from string import ascii_lowercase

import pandas as pd
import numpy as np

#website prefix
prefix = "http://www.basketball-reference.com"
#For store all webpages for players last name from a to z
profile_webpages = {}

#Use 'A' page (all players last name start with A) to get the hearder list for the table
webpage_a = urlopen('http://www.basketball-reference.com/players/a/').read()
soup_a = BeautifulSoup(webpage_a,'html5lib')
profile_header_list = []
#Fetch headers
profile_header = soup_a.find("table",{"id":"players"}).find("thead").find("tr")
for j in profile_header.find_all("th"):
    profile_header_list.append(j.get_text())
#Insert a player_id and player_url columns to the first
profile_header_list.insert(0,'player_id')
profile_header_list.insert(1,'player_url')
print profile_header_list

#Temp list to store profile table
t_profile = []
#loop a to z to get all players info expect x since no players' last name start with x:
for c in range(ord('a'), ord('w')+1)+ range(ord('y'), ord('z')+1):
    profile_webpages[c] = urlopen('http://www.basketball-reference.com/players/' + chr(c) +"/").read()
    profile_soup = BeautifulSoup(profile_webpages[c],'html5lib')

    #find the player profile for each player
    body = profile_soup.find("table",{"id":"players"}).find("tbody").findAll("tr")
    for i in body:
        #temp list to store player info
        s = []
        #player_id:
        s.append(i.find('th', {"class":"left ", "data-stat":"player"})["data-append-csv"])
        #player_url:
        s.append(prefix + i.find('th', {"class":"left ", "data-stat":"player"}).a["href"])
        #player name:
        s.append(i.find('th', {"class":"left ", "data-stat":"player"}).a.get_text())
        #All other player info:
        for k in i.find_all("td"):
            s.append(k.get_text())
        print s
        t_profile.append(s)

profile_table_all = pd.DataFrame(t_profile,columns=profile_header_list)
#Take only the players who have played during 2005/2006 to 2014/2015 seasons.
profile_table_all[['From','To']] = profile_table_all[['From','To']].apply(pd.to_numeric)
profile_table = profile_table_all[(profile_table_all.From<2016)&(profile_table_all.To>2005)]
print profile_table

profile_csv_path = 'player_profile.csv'
profile_table.to_csv(profile_csv_path)



        # players[element.a.get_text()]={}
        #
        # #Scrap each individual players' first year
        # name = element.find('th',{"class":"left", "data-stat":"player"}).a.get_text()
        # players[element.a.get_text()]["name"] = name
        #
        # #Scrap each individual players' URL link
        # players[element.a.get_text()]["link"] = prefix + element.a["href"]
        #
        # #Scrap each individual players' first year
        # year_min = element.find('td',{"class":"right", "data-stat":"year_min"}).get_text()
        # players[element.a.get_text()]["firstyear"] = year_min
        #
        # #Scrap each individual players' last year
        # year_max = element.find('td',{"class":"right", "data-stat":"year_max"}).get_text()
        # players[element.a.get_text()]["lastyear"] = year_max
        #
        # #Scrap each individual players' position
        # pos = element.find('td',{"class":"center ","data-stat":"pos"}).get_text()
        # players[element.a.get_text()]["position"] = pos
        #
        # #Scrap each individual players' height
        # height = element.find('td',{"class":"right ", "data-stat":"height"}).get_text()
        # players[element.a.get_text()]["height"] = height
        #
        # #Scrap each individual players' weight
        # weight = element.find('td',{"class":"right ", "data-stat":"weight"}).get_text()
        # players[element.a.get_text()]["weight"] = weight
        #
        # #Scrap each individual players' colleage name
        # try:
        #     college = element.find('td',{"class":"left ", "data-stat":"college_name"}).a.get_text()
        # except AttributeError:
        #     players[element.a.get_text()]["college"] = ''
        #     continue #skip to the next loop.
        # else:
        #     players[element.a.get_text()]["college"] = college


# for item in players.keys():
#     if int(players[item]["lastyear"])> 2004 & int(players[item]["firstyear"])< 2015:
#         print players[item]["name"] + ": " + "\n\t" + "link: " + players[item]["link"] + "\n\t" + "last year: " + players[item]["lastyear"] + "\n\t" + "college: " + players[item]["college"]

#
# for item in players.keys():
#
# webpage = urlopen('http://www.basketball-reference.com/players/a/allenra02.html').read()
# #print "<!--  \n    <div class=\"section_content\" id=\"div_transactions\"> \n    </div>\n\n-->  "
# #webpage =  "<!--  \n    <div class=\"section_content\" id=\"div_transactions\"> \n    </div>\n\n-->  "
#
# #re.sub(r"^\s+","",webpage,flags=re.MULTILINE)
#
# soup = BeautifulSoup(re.sub("<!--|-->","",webpage),'html5lib')
#
# #re.sub(r"<!--\s+\n\s+<div",r"\n<div",webpage,flags=re.MULTILINE)
# #re.sub(r"/div>\s+-->",r"/div>\n",webpage,flags=re.MULTILINE)
#
# #print webpage
#
# #soup = BeautifulSoup(webpage, "html.parser")
#
# print soup.prettify()
#
# header = soup.find("table",{"class":"suppress_glossary sortable stats_table","id":"all_salaries","data-cols-to-freeze":2 }).find("thead")
# table = soup.find("table",{"class":"suppress_glossary sortable stats_table","id":"all_salaries","data-cols-to-freeze":2}).find("tbody").findAll("tr")
#



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
