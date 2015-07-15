from bs4 import BeautifulSoup
import requests
root = "http://seattle.pydata.org"
url = "http://seattle.pydata.org/schedule/"
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data,"html.parser")
counter=1
for link in soup.find_all('a'):
    newurl = link.get('href')
    if 'presentation' in newurl:
        url1 = root+link.get('href')
        r1 = requests.get(url1)
        data1 = r1.text
        soup = BeautifulSoup(data1,"html.parser")
        print "---"
        print counter
        print "---"
        print url1.encode('utf-8')
        for s in soup.find_all('h4'):
            if "Sponsors" not in s.text:
                dat = s.text
                data = dat.strip()
                print dat.encode('utf-8')
        # print "Time: "+soup.find('h4').string
        print "Title: "+soup.find('h2').string.encode('utf-8')
        print "Speaker: "+soup.find('h4').string.encode('utf-8')



        description = soup.find('div', class_="description").text
        print "Description: " + description.encode('utf-8')
        abstract = soup.find('div', class_="abstract")
        print "Abstract: "+abstract.text.encode('utf-8')
        print "\n"
        counter+=1
