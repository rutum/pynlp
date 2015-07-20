from bs4 import BeautifulSoup
import requests
import ujson as json
from unidecode import unidecode

root = "http://seattle.pydata.org"
url = "http://seattle.pydata.org/schedule/"
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data,"html.parser")
counter=1
fout = open("data_file.txt", "w")
alldata = {}

def cleanup(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = text.replace("\"","\'")
    return(text)

for link in soup.find_all('a'):
    newurl = link.get('href')
    newdict = {}
    if 'presentation' in newurl:
        url1 = root+link.get('href')
        r1 = requests.get(url1)
        data1 = r1.text
        soup = BeautifulSoup(data1,"html.parser")
        for s in soup.find_all('h4'):
            if "Sponsors" not in s.text:
                dat = s.text
                dat = dat.strip()
                if unicode(dat):
                    dat = unidecode(dat)
                data = ' '.join(dat.split())
                if "a.m." in data or "p.m." in data:
                    newdict["time"] = data
        title = soup.find('h2').string
        newdict["title"] = cleanup(unidecode(title))
        description = soup.find('div', class_="description").text
        newdict["description"] = cleanup(unidecode(description))
        abstract = soup.find('div', class_="abstract")
        newdict["abstract"] = cleanup(unidecode(abstract.text))
        counter+=1
        json.dump(newdict, fout)
        fout.write("\n")
fout.close()
