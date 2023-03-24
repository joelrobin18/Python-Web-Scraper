import requests
from bs4 import BeautifulSoup
import pandas as pd

# Match Deatails Scraper Code
url = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'engineTable'})

# print(table)

match_summary=[]
# Extract the data from the table
rows = table.find_all('tr', {'class': ['data1', 'data2']})
for row in rows:
    cols = row.find_all('td')
    temp=[]
    
    # print(cols)
    
    team1 = cols[0].text.strip()
    temp.append(team1)
    team2 = cols[1].text.strip()
    temp.append(team2)
    result = cols[2].text.strip()
    temp.append(result)
    margin = cols[3].text.strip()
    temp.append(margin)
    Venue = cols[4].text.strip()
    temp.append(Venue)
    Date = cols[5].text.strip()
    temp.append(Date)
    Match_id = cols[6].text.strip()
    temp.append(Match_id)

    match_summary.append(temp)
    
    # print(f'{team1} vs {team2} | Result: {result} | margin: {margin} | Venue: {Venue} | Date: {Date} | Match ID: {Match_id}')
    
print(match_summary)
match = pd.DataFrame(match_summary)
print(match.head())

match.rename(columns={0:"Team1",1:"Team2",2:"Result",3:"Margin",4:"Venue",5:"Date",6:"Match ID"},inplace=True)
match.to_csv("match_summary.csv")

#Links for each Match Scraper
links = []
for i,link in enumerate(table.find_all("a")):
    if "team" not in link.get("href") and "ground" not in link.get("href"):
        links.append(link.get("href"))

print(links)
scorecard_link = pd.DataFrame(links)

print(scorecard_link.head())
scorecard_link.rename(columns={0:"Link"},inplace=True)
scorecard_link.to_csv("Link.csv")


#Scorecard Scraper Python Code
i=0

score_card=[]

for link in links:
    url_check = "https://stats.espncricinfo.com" + link
    
    response_link = requests.get(url_check)
    
    soup_check = BeautifulSoup(response_link.content,'html.parser')
    
    tables_link = soup_check.find_all('table',{'class':'ci-scorecard-table'})
    
    # match_scorecard=[]
    
    # # print(table_link)
    for table_link in tables_link:
        if table_link is not None:
            rows_check = table_link.find_all('tr')
            # print(rows_check)
            
            innings_scorecard = []
            
            for row in rows_check:
                
                col = row.find_all('td')
                # print(col)
                if len(col) > 4:
                    name = col[0].text.strip()
                    dismisal = col[1].text.strip()
                    runs = col[2].text.strip()
                    balls = col[3].text.strip()
                    
                    minutes = col[4].text.strip()
                    fours = col[5].text.strip()
                    sixes = col[6].text.strip()
                    strike_rate = col[7].text.strip()
                    
                    # print(f"Name: {name } | Dismissal: {dismisal} | Runs: {runs}: {runs} | Ball : {balls} | Minuts: {minutes} | Fours: {fours} | Sixes: {sixes} | Strike rate: {strike_rate}")
                    innings_scorecard.append([name,dismisal,runs,balls,minutes,fours,sixes,strike_rate])
            # match_scorecard.append(innings_scorecard)
            score_card.extend(innings_scorecard)
            print("match: ",i)
            i=i+1
    
    # print(len(score_card))

scorecard = pd.DataFrame(score_card)
scorecard.rename(columns={0:"Batsman",1:"Dismisal",2:"Runs",3:"Balls",4:"Minutes Batted",5:"Fours",6:"Sixes",7:"Strike Rate"},inplace=True)
print(scorecard.tail(22))

scorecard.to_csv("scorecard.csv")


# Bowling Summary Scraper Python Code
i=0
bowling_summary=[]
for link in links:
    url_check = "https://stats.espncricinfo.com" + link
    
    response_link = requests.get(url_check)
    
    soup_check = BeautifulSoup(response_link.content,'html.parser')
    
    tables_link = soup_check.find_all('table')
    
    bowling_datas_team1 = tables_link[1].find_all("tr")
    for datas in bowling_datas_team1:
        data = datas.find_all("td") 
        if len(data) >4:
            bowler =  data[0].text.strip()
            over = data[1].text.strip()
            maiden = data[2].text.strip()
            runs = data[3].text.strip()
            wicket = data[4].text.strip()
            economy = data[5].text.strip()
            dot = data[6].text.strip()
            fours = data[7].text.strip()
            sixes= data[8].text.strip()
            wide = data[9].text.strip()
            no_balls = data[10].text.strip()
            bowling_summary.append([bowler,over,maiden,runs,wicket,economy,dot,fours,sixes,wide,no_balls])
            # print(len(bowling_summary))
            # print(bowler,over,maiden,wicket,economy,dot,fours,sixes,wide,no_balls)
    i=i+1
    print("Innings: ",i)
    
    bowling_datas_team2 = tables_link[1].find_all("tr")
    for datas in bowling_datas_team2:
        data = datas.find_all("td") 
        if len(data) >4:
            bowler =  data[0].text.strip()
            over = data[1].text.strip()
            maiden = data[2].text.strip()
            runs = data[3].text.strip()
            wicket = data[4].text.strip()
            economy = data[5].text.strip()
            dot = data[6].text.strip()
            fours = data[7].text.strip()
            sixes= data[8].text.strip()
            wide = data[9].text.strip()
            no_balls = data[10].text.strip()
            bowling_summary.append([bowler,over,maiden,runs,wicket,economy,dot,fours,sixes,wide,no_balls])
            # print(len(bowling_summary))
            # print(bowler,over,maiden,wicket,economy,dot,fours,sixes,wide,no_balls)
    i=i+1
    print("Innings: ",i)
    
bowling_dataframe = pd.DataFrame(bowling_summary)
bowling_dataframe.rename(columns={0:"Bowler",1:"Overs",2:"Maidens",3:"Runs",4:"Wickets",5:"Economy",6:"Dot Balls",7:"Fours",8:"Sixes",9:"Wide",10:"No Balls"},inplace=True)
print(bowling_dataframe.head())

bowling_dataframe.to_csv("bowling_summary.csv")


# Players details Summary

player_details = []
for link in links:
    url_check = "https://stats.espncricinfo.com" + link
    response_link = requests.get(url_check)
    soup_check = BeautifulSoup(response_link.content,'html.parser')
    tables_link = soup_check.find_all('table',{'class':'ci-scorecard-table'})

    for table in tables_link:
        player_link = table.find_all("a")

        for i in player_link:
            player_link = "https://www.espncricinfo.com" + i.get("href") 
            print(player_link)
            
            player_detail_link = requests.get(player_link)
            soup_player = BeautifulSoup(player_detail_link.content,'html.parser')
            
            divs = soup_player.find_all("div")
            for div in divs:
                if len(div) > 1:
                    heading = div.find_all("p")
                    value = div.find_all("span")
                    
                    if len(heading)>1:
                        
                        if heading[0].text.strip() =="Full Name" and heading[1].text.strip() =="Born" and heading[2].text.strip() =="Age":
                            if len(value) >1:
                                name = value[0].text.strip()
                                born = value[1].text.strip()
                                age = value[2].text.strip()
                                batting = value[3].text.strip()
                                role = value[4].text.strip()
                                
                                player_details.append([name, born, age, batting, role])
                                # print(name, born, age, batting, role)
            # number=number+1
            # print("Player: ",number)

unique_list=[]

# Delete all the duplicate elements
for x in player_details:
    if x not in unique_list:
        unique_list.append(x)

# Delete all the unwanted datas
temp=[]
for x in unique_list:
    if x[0] != "Overview":
        temp.append(x)

players_dataframe = pd.DataFrame(temp)
players_dataframe.rename(columns={0:"Name",1:"DOB",2:"Age",3:"Batting_Style",4:"Role"},inplace=True)

print(players_dataframe.head())

players_dataframe.to_csv("players_details.csv")