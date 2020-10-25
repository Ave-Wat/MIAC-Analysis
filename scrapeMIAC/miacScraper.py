"""
python3 -m venv 'name'-env
'name'-env\Scripts\activate.bat
pip install bs4 or sudo pip3 install bs4
pip install requests or sudo pip3 install requests
"""

from bs4 import BeautifulSoup
import requests
import csv
import tabula

headers = requests.utils.default_headers()
headers.update({
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
})

def scrape2018Champ(url):
    athleteOutputList = []

    response = requests.get(url, headers = headers)
    content = BeautifulSoup(response.content, "html.parser")

    resultsList = content.find_all('table')

    for line in resultsList[1].find_all('tr'):
            sectionList = line.find_all('td')
            if sectionList[0].getText().isnumeric() is True:
                event = 'MIAC Championships'
                name = sectionList[1].getText()
                team = sectionList[2].getText()
                time = sectionList[13].getText()
                place = sectionList[0].getText()
                year = '2018'
                location = 'St. Olaf'

                athleteDict = {'event':event, 'name':name, 'team':team, 'time':time, 'place':place, 'year':year, 'location':location}
                athleteOutputList.append(athleteDict)

    writeToCSV("2014MIAC.csv", athleteOutputList)

    return athleteOutputList

def scrape2017Champ(url):
    athleteOutputList = []

    response = requests.get(url, headers = headers)
    content = BeautifulSoup(response.content, "html.parser")

    resultsList = content.find_all('table')

    for line in resultsList[1].find_all('tr'):
            sectionList = line.find_all('td')
            if sectionList[0].getText().strip().isnumeric() is True:
                event = 'MIAC Championships'
                name = sectionList[3].getText().strip()
                team = sectionList[4].getText().strip()
                time = sectionList[5].getText().strip()
                place = sectionList[0].getText().strip()
                year = '2017'
                location = 'St. Olaf'

                athleteDict = {'event':event, 'name':name, 'team':team, 'time':time, 'place':place, 'year':year, 'location':location}
                athleteOutputList.append(athleteDict)

    writeToCSV("2014MIAC.csv", athleteOutputList)

    return athleteOutputList

def scrape2016Champ():
    # needs to be reordered to correct format in csv
    file = "2016_MIAC_MXC_Results.pdf"
    tabula.convert_into(file, "2016MIAC.csv", pages = "all")

def scrape2015Champ():
    #isn't working for SHIT
    file = "2015_MIAC_MXC_Results.pdf"
    tabula.convert_into(file, "2015MIAC.csv", pages = [2,3,4,5,6,7,8,9,10])

def scrape2014Champ():
    # need to amend data in csv
    url = "https://www.miacathletics.com/playoffs/2014-15/XC_2014/miacmencc2014.html"
    athleteOutputList = []
    
    response = requests.get(url, headers = headers)
    content = BeautifulSoup(response.content, "html.parser")

    paragraphList = content.find_all('p')

    table = paragraphList[8].getText()
    lines = table.split('\n')
    lines = lines[1:-2] # had to get rid of blank lines

    j = 0
    for line in lines:
        if j != 156 and j != 157:
            lineList = line.split("  ")
            '''place, place, name-grade, time, school'''
            while '' in lineList:
                lineList.remove('')

            for i in range(0, len(lineList)):
                lineList[i] = lineList[i].strip()
            if lineList[1].isnumeric():
                lineList.pop(1)

            nameGradeList = lineList[1].split(",")

            event = 'MIAC Championships'
            name = nameGradeList[0]
            team = lineList[3]
            time = lineList[2]
            place = lineList[0]
            year = '2014'
            location = 'Como Golf Course, St. Paul'

            athleteDict = {'event':event, 'name':name, 'team':team, 'time':time, 'place':place, 'year':year, 'location':location}
            athleteOutputList.append(athleteDict)
        if j == 156: # the website is messed up on this particular line
            list = ['Ernest Polania-Gonzalez','So','29:11.6','Carleton']
            athleteDict = {'event':'MIAC Championships', 'name':list[0], 'team':list[3], 'time':list[2], 'place':'157', 'year':'2014', 'location':'Como Golf Course, St. Paul'}
            athleteOutputList.append(athleteDict)
        j = j + 1

    writeToCSV("2014MIAC.csv", athleteOutputList)

def writeToCSV(filename, athleteOutputList):
    keys = athleteOutputList[0].keys()
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, keys)
        writer.writerows(athleteOutputList)
        file.close()

def main():
    fastFinishList = ['https://www.miacathletics.com/playoffs/2018-19/xc18/Men8kResults.htm', 'https://www.miacathletics.com/sports/mxc/2017-18/files/MIACMen.html']
    athleteList = []
    scrape2018Champ("https://www.miacathletics.com/playoffs/2018-19/xc18/Men8kResults.htm")
    scrape2017Champ("https://www.miacathletics.com/sports/mxc/2017-18/files/MIACMen.html")
    scrape2016Champ()
    scrape2015Champ()
    scrape2014Champ()

main()