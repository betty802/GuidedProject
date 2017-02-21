from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import re
import html5lib
import pandas as pd
import numpy as np
import time
import httplib

player_profile = pd.DataFrame(pd.read_csv("player_profile.csv"))
player_urls = player_profile['player_url'].tolist()

# Creating objects
# Temp list to append header and content later
pergame_header_list = []
t_pergame = []
# Temp list to append header and content later
salary_header_list = []
t_salary = []

time.sleep(0.5)
# Take the first player page to fetch all headers for per game and salary tables:
webpage = urlopen(player_urls[0]).read()
soup = BeautifulSoup(re.sub("<!--|-->", "", webpage), 'html5lib')
# Fetch headers for pergame table
pergame_header = soup.find("table", {"id": "per_game"}).find("thead").find("tr")
for j in pergame_header.find_all("th"):
    pergame_header_list.append(j.get_text())
#Insert a player id column in the header
pergame_header_list.insert(0,'player_id')
print pergame_header_list
# Fetch headers for salary table
salary_header = soup.find("table", {"class": "suppress_glossary sortable stats_table", "id": "all_salaries"}).find(
    "thead").find("tr")
for j in salary_header.find_all("th"):
    salary_header_list.append(j.get_text())
#Insert a player id column in the header
salary_header_list.insert(0,'player_id')
print salary_header_list


for i in player_urls:
    try:
        time.sleep(1)
        webpage = urlopen(i).read()
        soup = BeautifulSoup(re.sub("<!--|-->", "", webpage), 'html5lib')
        # find the player tables
        pergame_soup = soup.find("table", {"id": "per_game"}).find("tbody").findAll("tr", {"class": "full_table"})
        #Strip out player id from the gamelog url
        player_id=(pergame_soup[0].find('th', {"class": "left ", "data-stat": "season"}).a["href"]).split('/')[3]

        for i in pergame_soup:
            s = []
            s.append(player_id)
            s.append(i.find('th', {"class": "left ", "data-stat": "season"}).a.get_text())
            for k in i.find_all("td"):
                s.append(k.get_text())
            print s
            t_pergame.append(s)

        # salary_table = salary_table.append(salary_header_list, ignore_index=True)

        salary_soup = soup.find("table", {"class": "suppress_glossary sortable stats_table", "id": "all_salaries"}).find(
            "tbody").findAll("tr")
        for i in salary_soup:
            s = []
            s.append(player_id)
            s.append(i.find("th").get_text())
            for k in i.find_all("td"):
                s.append(k.get_text())
            print s
            t_salary.append(s)
    except:
        AttributeError
        httplib.IncompleteRead
        continue

pergame_table = pd.DataFrame(t_pergame, columns=pergame_header_list)
print pergame_table
salary_table = pd.DataFrame(t_salary, columns=salary_header_list)
print salary_table

pergame_csv_path = 'player_pergame.csv'
salary_csv_path = 'player_salary.csv'
pergame_table.to_csv(pergame_csv_path)
salary_table.to_csv(salary_csv_path)

# df = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
#
# for element in salary:
#     player_salary[element.a.get_text()] = {}
#
#     # Scrap each individual player_salary' first year
#     name = element.find('th', {"class": "left", "data-stat": "player"}).a.get_text()
#     player_salary[element.a.get_text()]["name"] = name
#
# soup = BeautifulSoup(re.sub("<!--|-->", "", webpage), 'html5lib')
#
# # re.sub(r"<!--\s+\n\s+<div",r"\n<div",webpage,flags=re.MULTILINE)
# # re.sub(r"/div>\s+-->",r"/div>\n",webpage,flags=re.MULTILINE)
#
# # print webpage
#
# # soup = BeautifulSoup(webpage, "html.parser")
#
# print soup.prettify()
#
# header = soup.find("table", {"class": "suppress_glossary sortable stats_table", "id": "all_salaries",
#                              "data-cols-to-freeze": 2}).find("thead")
# table = soup.find("table", {"class": "suppress_glossary sortable stats_table", "id": "all_salaries",
#                             "data-cols-to-freeze": 2}).find("tbody").findAll("tr")

# table1 = soup.find("table",{"id":"per_game"}).findAll("tr",{"class":"light_text partial_table"})
# file name

# out = open('rayallen.csv', 'w')
#
# # print header
# for j in header.find_all("th"):
#     out.write(j.get_text() + ",")
# out.write("\n")
# # print table
# for i in table:
#     d = i.find("th");
#     out.write(d.get_text() + ",")
#     for j in i.find_all("td"):
#         out.write(j.get_text() + ",")
#     out.write("\n")

# for i in table1:
#    d = i.find("th");
#   out.write(d.get_text() + ",")
#   for j in i.find_all("td"):
#       out.write(j.get_text() + ",")
#  out.write("\n")
# out.close()
print 'Done!'
