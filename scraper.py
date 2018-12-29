#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Twitter import TwitterMsg

from bs4 import BeautifulSoup
import pandas as pd

import time

global allgamesdf
global userids

path = '/Users/vpetrov/PycharmProjects/FootballAPI/'


def scrapesite():

    # open website
    options = Options()
    options.headless = True

    driver = webdriver.Chrome('/Users/vpetrov/PycharmProjects/FootballAPI/venv/bin/chromedriver', options=options)
    driver.get('http://www.google.com/xhtml')

    time.sleep(1) # Let the user actually see something!

    driver.get("https://www.flashscore.com/football/")

    wait = WebDriverWait(driver, 1)

    # live_games_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "LIVE Games")))
    #live_games_link.click()

    table_main = driver.find_element_by_class_name('table-main')
    soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

    table = soup.prettify()

    f = open('text.txt', 'w', encoding='utf-8')
    f.write(table)
    f.close()

    driver.quit()


def extractlivescores():

    global allgamesdf

    f = open('text.txt', 'r', encoding='utf-8')
    lines = f.read().replace('\n', '')

    soup = BeautifulSoup(lines, 'html.parser')

    cols = ['progress','timer','nation','league','time_of_match', 'team_home', 'team_away', 'score', 'hgoals', 'ggoals', 'htscore', 'hthgoals', 'htggoals', 'redcard', 'match_id']
    allgamesdf = pd.DataFrame(columns=cols)

    for table in soup.findAll("table", {"class": 'soccer'}):
        nation = str.replace(table.find("span", {"class": 'country_part'}).text, ':', '')
        league = table.find("span", {"class": 'tournament_part'}).text

        trs_live = table.findAll("tr", {"class": lambda x: x and "stage-live" in x.split()})
        trs_finished = table.findAll("tr", {"class": lambda x: x and "stage-finished" in x.split()})
        trs_scheduled = table.findAll("tr", {"class": lambda x: x and "stage-scheduled" in x.split()})

        trs = trs_live + trs_finished + trs_scheduled

        #print('found {} trs for {}: '.format(len(trs), nation))

        for index, tr in enumerate(trs):
            
            time_of_match = tr.find("td", {"class": lambda x: x and "time" in x.split()}).text
            team_home = tr.find("td", {"class": lambda x: x and "team-home" in x.split()}).text
            team_away = tr.find("td", {"class": lambda x: x and "team-away" in x.split()}).text

            #print("checking {}".format(team_home))

            if tr.find("span", {"class": lambda x: x and "final_result_only" in x.split()}):
                # print("skipping {}".format(team_home))
                break

            match_id = tr.get('id').split('_')[-1]

            classes = tr.get('class')

            htscore = ''
            timer = ''
            score = ''
            hgoals = ''
            ggoals = ''
            hthgoals = ''
            htggoals = ''
            redcard = ''
            progress = ''

            if any(x in ['stage-live', 'stage-finished'] for x in classes):
                if 'stage-live' in classes:
                    progress = 'live'
                    htscore = tr.find("td", {"class": lambda x: x and "part-top" in x.split()}).text
                    try:
                        hthgoals = htscore.replace("(", "").split('-')[0]
                        htggoals = htscore.replace(")", "").split('-')[1]
                    except:
                        htggoals = 0
                        htggoals = 0
                else: progress = 'finished'

                score = tr.find("td", {"class": lambda x: x and "score" in x.split()}).text
                hgoals = score.split('-')[0]
                ggoals = score.split('-')[1]
                timer = tr.find("td", {"class": lambda x: x and "timer" in x.split()}).text

                redcardh = ''
                redcarda = ''

                if tr.find("span", {"class": lambda x: x and "rhcard" in x.split()}):
                    redcardh = 'home'
                if tr.find("span", {"class": lambda x: x and "racard" in x.split()}):
                    redcarda = 'away'
                redcard = redcardh + redcarda
                
            elif 'stage-scheduled' in classes:
                progress = 'scheduled'

            elif 'stage-finished' in classes:
                progress = 'finished'

            row = list(map(str.strip,[progress, timer, nation, league, time_of_match, team_home, team_away, score, hgoals, ggoals, htscore, hthgoals, htggoals, redcard, match_id]))
            allgamesdf = allgamesdf.append(pd.DataFrame([row], columns=cols), ignore_index=True)
    # print(df)
    f.close()

    allgamesdf.loc[allgamesdf['timer'].isin(['Half Time', '45+', 'Finished','Postponed']),'timer']=0
    allgamesdf['timer'] = allgamesdf['timer'].str.extract('(\d+)')#.astype(int)
    allgamesdf['timer'] = allgamesdf['timer'].infer_objects().fillna(0)
    allgamesdf.sort_values('time_of_match', inplace=True)
    allgamesdf.to_csv(path + 'allgames.csv', index=False)
    # TwitterMsg.sendDM(userids=userids, msg='There are {} games live'.format(len(allgamesdf)))


def addwatchlistinfo():
    global allgamesdf

    values = {'fhg': '', 'shg': ''}
    watchlist = pd.read_csv(path + 'watchlist.csv')
    watchlist['Match'] = watchlist['Match'].str.strip()
    watchlist['team_home'], watchlist['team_away'] = watchlist['Match'].str.split(' v ', 1).str
    watchlist = watchlist[["team_home","team_away","fhg","shg"]].fillna(value= values)
    watchlist.to_csv(path + 'watchlistnew.csv', index=False)

    allgamesdf = allgamesdf.merge(watchlist, on=['team_home','team_away'], how='left')
    allgamesdf.to_csv(path + 'allgames.csv', index=False)


def findlateshg():
    livegames = allgamesdf[(allgamesdf['progress'] == 'live')]
    lategames = livegames[(livegames['timer'].astype(int) > 60)]
    shg_watch = lategames[lategames['shg'] == 'x']

    if not lategames.empty:
        print('###################################')
        print('#            Late SHG             #')
        print('###################################')

        msg_list = '###### SHG from List Alert #######\n'
        msg_late00 = '###### SH 0-0 Alert #######\n'
        for index, row in lategames.iterrows():
            summary = 'Reached {}\' in {} - {} ({}) at {}-{}'.format(row['timer'],row['team_home'],row['team_away'],row['nation'],row['hgoals'],row['ggoals']) + '\n' + \
                    'Check stats at https://www.flashscore.com/match/{}/#match-statistics;0\n'.format(row['match_id'])

            print('Checking {} - {} ({}-{})'.format(row['team_home'],row['team_away'],row['hgoals'],row['ggoals']))
            if row['shg'] == 'x' and row['hgoals'] == row['hthgoals'] and row['ggoals'] == row['htggoals']:
                msg_list = msg_list + summary
                TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "SHG_list", msg_list))

            elif row['hgoals'] == '0' and row['ggoals'] == '0':
                print('added game to msg_late00')
                msg_late00 = msg_late00 + summary
                TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "SHG", msg_late00))
    else:
        print("no SHG candidates \n")


def findfhg():

    livefhgames = ''
    livefhgames = allgamesdf[(allgamesdf['progress'] == 'live') & (allgamesdf['timer'].astype(int) < 46)]
    print('\n{} live FH games found'.format(len(livefhgames)))

    latefhgames = livefhgames[(livefhgames['timer'].astype(int) > 30)]
    fhg_watch = latefhgames[latefhgames['fhg'] == 'x']

    if not latefhgames.empty:
        print('###################################')
        print('#           Late FHG              #')
        print('###################################')

        msg_list = '###### FHG from List Alert #######\n'
        msg_late00 = '###### FH still 0-0 Alert #######\n'
        for index, row in latefhgames.iterrows():
            summary = 'Reached {}\' in {} - {} ({}) at {}-{}'.format(row['timer'],row['team_home'],row['team_away'],row['nation'],row['hgoals'],row['ggoals']) + '\n' + \
                    'Check stats at https://www.flashscore.com/match/{}/#match-statistics;0\n'.format(row['match_id'])

            print('Checking {} - {} ({}-{})'.format(row['team_home'],row['team_away'],row['hgoals'],row['ggoals']))
            if row['fhg'] == 'x':
                msg_list = msg_list + summary
                TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "FHG_list", msg_list))
            elif row['hgoals'] == '0' and row['ggoals'] == '0':
                msg_late00 = msg_late00 + summary
                TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "FHG", msg_late00))
    else:
        print("no FHG candidates \n")


def matchsummary():

    games = pd.read_csv(path + 'allgames.csv')


def dumpmatchsummary():
    import os

    games = pd.read_csv(path + 'allgames.csv')

    # open website
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(path + '/venv/bin/chromedriver', options=options)
    driver.get('http://www.google.com/xhtml')

    time.sleep(1) # Let the user actually see something!

    for index, row in games.iterrows():
        match_id = row['match_id']

        if row['progress'] == 'scheduled':

            exists = os.path.isfile(path + '/matches/pmodds/{}.txt'.format(match_id))

            if not exists:
                url = 'https://www.flashscore.com/match/{}/#odds-comparison;1x2-odds;full-time'.format(match_id)
                print('getting {}'.format(url))

                driver.get(url)
                #wait = WebDriverWait(driver, 10)
                time.sleep(1)

                table = ''
                try:
                    table_main = driver.find_element_by_id('odds_1x2')
                    soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

                    table = soup.prettify()
                except:
                    print('Cannot find odds_1x2 class in {}'.format(url))

                f = open(path + 'matches/pmodds/{}.txt'.format(match_id), 'w', encoding='utf-8')
                f.write(table)
                f.close()
            else:
                print('file odds already exists {}'.format(match_id))

    driver.quit()

def extractpmodds():
    import os

    directory = os.fsencode(path + '/matches/pmodds/')

    for file in os.listdir(directory):
        lines = open(directory + file).read().replace('\n', '')
        soup = BeautifulSoup(lines, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                print(td.get_text())




userids = ['1208132010', '442751368']
userids = ['442751368']
scrapesite()
extractlivescores()
addwatchlistinfo()
findlateshg()
findfhg()
dumpmatchsummary()
#extractpmodds()

# dumpmatchsummary(['6mfA2XzG','4t3Whcfb'])
