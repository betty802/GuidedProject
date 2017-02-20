from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
import csv
import html5lib

#webpage passed from kaixiang
webpage = urlopen('http://www.basketball-reference.com/players/a/allenra02.html').read()
#print "<!--  \n    <div class=\"section_content\" id=\"div_transactions\"> \n    </div>\n\n-->  "
#webpage =  "<!--  \n    <div class=\"section_content\" id=\"div_transactions\"> \n    </div>\n\n-->  "

#re.sub(r"^\s+","",webpage,flags=re.MULTILINE)

soup = BeautifulSoup(re.sub("<!--|-->","",webpage),'html5lib')

#re.sub(r"<!--\s+\n\s+<div",r"\n<div",webpage,flags=re.MULTILINE)
#re.sub(r"/div>\s+-->",r"/div>\n",webpage,flags=re.MULTILINE)

#print webpage

#soup = BeautifulSoup(webpage, "html.parser")

print soup.prettify()

header = soup.find("table",{"class":"suppress_glossary sortable stats_table","id":"all_salaries","data-cols-to-freeze":2 }).find("thead")
table = soup.find("table",{"class":"suppress_glossary sortable stats_table","id":"all_salaries","data-cols-to-freeze":2}).find("tbody").findAll("tr")

#table1 = soup.find("table",{"id":"per_game"}).findAll("tr",{"class":"light_text partial_table"})
#file name

out = open('rayallen.csv', 'w')

# print header
for j in header.find_all("th"):
    out.write(j.get_text() + ",")
out.write("\n")
# print table
for i in table:
    d = i.find("th");
    out.write(d.get_text() + ",")
    for j in i.find_all("td"):
        out.write(j.get_text() + ",")
    out.write("\n")

#for i in table1:
#    d = i.find("th");
 #   out.write(d.get_text() + ",")
 #   for j in i.find_all("td"):
 #       out.write(j.get_text() + ",")
  #  out.write("\n")
out.close()
print 'Done!'
