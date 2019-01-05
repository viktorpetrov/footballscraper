#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Twitter import TwitterMsg
from Telegram import Telegram

from bs4 import BeautifulSoup
import pandas as pd

import time
import os
import datetime

from localsettings import *

global allgamesdf
global userids

teamnames = {
    'Al Ittifaq': 'Al-Ettifaq',
    'Al Ittihad': 'Al-Ittihad FC',
    'Hamilton Academical': 'Hamilton',
    'Maccabi Netanya': 'Netanya',
    'Ironi Kiryat Shmona': 'Shmona',
    'Alloa Athletic': 'Alloa',
    'Dundee United': 'Dundee Utd',
    'Mansfield Town': 'Mansfield',
    'Harlow Town': 'Harlow',
    'Fleetwood Town': 'Fleetwood',
    'MacaÃ©': 'Macae',
    'Chelmsford City': 'Chelmsford',
    'Ballymena United': 'Ballymena',
    'Accrington Stanley': 'Accrington',
    'Chesham United': 'Chesham',
    'Notts County': 'Notts Co',
    'West Bromwich Albion': 'West Brom',
    'Taunton Town': 'Taunton',
    'St Ives Town': 'St. Ives',
    'Sutton United': 'Sutton',
    'Exeter City': 'Exeter',
    'Harrow Borough': 'Harrow',
    'Dorking Wanderers': 'Dorking',
    'Carlisle United': 'Carlisle',
    'Warrenpoint Town': 'Warrenpoint',
    'Swindon Supermarine': 'Swindon S',
    'Gosport Borough': 'Gosport',
    'Newport County': 'Newport Co',
    'Leeds United': 'Leeds',
    'Maidenhead United': 'Maidenhead',
    'Torquay United': 'Torquay',
    'Hungerford Town': 'Hungerford',
    'AFC Telford United': 'AFC Telford',
    'Halesowen Town': 'Halesowen',
    'Oxford United': 'Oxford Utd',
    'Stockport County': 'Stockport',
    'Rushall Olympic': 'Rushall',
    'Havant & Waterlooville': 'Havant & W',
    'Ebbsfleet United': 'Ebbsfleet',
    'Dungannon Swifts': 'Dungannon',
    'Potters Bar Town': 'Potters Bar',
    'Scunthorpe United': 'Scunthorpe',
    'Brackley Town': 'Brackley',
    'Hapoel Raanana': 'H. Raanana',
    'Tottenham Hotspur': 'Tottenham',
    'Poole Town': 'Poole',
    'East Thurrock United': 'East Thurrock',
    'Haringey Borough (9)': 'Haringey',
    'Brightlingsea Regent': 'Brightlingsea',
    'Cheltenham Town': 'Cheltenham',
    'Frome Town': 'Frome',
    'Queens Park Rangers': 'Queen\'s Park',
    'Hapoel Beer Sheva': 'H. Beer Sheva',
    'Chippenham Town': 'Chippenham',
    'Swansea City': 'Swansea',
    'Burton Albion': 'Burton',
    'St Albans City': 'St. Albans',
    'United of Manchester': 'FC United',
    'Boston United': 'Boston Utd',
    'Merthyr Town': 'Merthyr T',
    'Merstham (16)': 'Merstham',
    'Slough Town': 'Slough',
    'Spennymoor Town': 'Spennymoor',
    'Truro City': 'Truro',
    'Newry City AFC': 'Newry City',
    'Dundee Utd.': 'Dundee Utd.',
    'Annan Athletic': 'Annan',
    'Bradford Park Avenue': 'Bradford PA',
    'Wycombe Wanderers': 'Wycombe',
    'Lowestoft Town': 'Lowestoft',
    'Basingstoke Town': 'Basingstoke',
    'Tiverton Town': 'Tiverton',
    'Wigan Athletic': 'Wigan',
    'Rotherham United': 'Rotherham',
    'Brechin City': 'Brechin',
    'Braintree Town': 'Braintree',
    'Newcastle United': 'Newcastle',
    'Swindon Town': 'Swindon',
    'Sheffield Wednesday': 'Sheffield Wed',
    'Doncaster Rovers': 'Doncaster',
    'Gloucester City': 'Gloucester',
    'Redditch United': 'Redditch',
    'Staines Town': 'Staines',
    'Plymouth Argyle': 'Plymouth',
    'Crawley Town': 'Crawley',
    'Macclesfield Town': 'Macclesfield',
    'Coalville Town': 'Coalville',
    'Banbury United': 'Banbury',
    'Shrewsbury Town': 'Shrewsbury',
    'Metropolitan Police FC': 'Met. Police FC',
    'Hull City': 'Hull',
    'Billericay Town': 'Billericay',
    'Nuneaton Town': 'Nuneaton',
    'Forest Green Rovers': 'Forest Green',
    'Sporting CP': 'Sporting',
    'Peterborough United': 'Peterborough',
    'Ashton United': 'Ashton Utd',
    'Aldershot Town': 'Aldershot',
    'St Neots Town': 'St. Neots',
    'Kidderminster Harriers': 'Kidderminster',
    'Salford City': 'Salford',
    'Ashdod': 'Moadon Sport Ashdod',
    'Hemel Hempstead Town': 'Hemel Hempstead',
    'Nova Iguacu': 'Nova Iguacu',
    'Grimsby Town': 'Grimsby',
    'Royston Town': 'Royston',
    'Alfreton Town': 'Alfreton',
    'Al Raed': 'Al-Raed',
    'ES Metlaoui': 'Metlaoui',
    'Kirinya Jinja SS': 'Jinja',
    'Man Utd': 'Manchester Utd',
    'Ohod Madinah': 'Ohod',
    'Uganda Police FC': 'Police',
    'Hapoel Ramat HaSharon': 'Ramat Hasharon',
    'Beitar Tel Aviv Ramla': 'Beitar Tel Aviv',
    'York City': 'York',
    'Crewe Alexandra': 'Crewe',
    'Lancaster City': 'Lancaster',
    'Stalybridge Celtic': 'Stalybridge',
    'Leicester City': 'Leicester',
    'Witton Albion': 'Witton',
    'Haringey Borough': 'Haringey',
    'Eastbourne Borough': 'Eastbourne Boro',
    'Gainsborough Trinity': 'Gainsborough',
    'Norwich City': 'Norwich',
    'Cardiff City': 'Cardiff',
    'North Ferriby United': 'North Ferriby',
    'Luton Town': 'Luton',
    'Nantwich Town': 'Nantwich',
    'Dorchester Town': 'Dorchester',
    'Hednesford Town': 'Hednesford',
    'Bala Town': 'Bala',
    'Cefn Druids': 'Druids',
    'Welling United': 'Welling',
    'Oldham Athletic': 'Oldham',
    'Kettering Town': 'Kettering',
    'Blyth Spartans': 'Blyth',
    'Derby County': 'Derby',
    'Western Sydney Wanderers': 'WS Wanderers W',
    'Hitchin Town': 'Hitchin',
    'Fylde': 'AFC Fylde',
    'Concord Rangers': 'Concord',
    'Farsley Celtic': 'Farsley',
    'Folkestone Invicta': 'Folkestone',
    'Southend United': 'Southend',
    'Sheffield United': 'Sheffield Utd',
    'Burgess Hill Town': 'Burgess Hill',
    'Stratford Town': 'Stratford',
    'Matlock Town': 'Matlock',
    'Bath City': 'Bath',
    'Colchester United': 'Colchester',
    'Preston North End': 'Preston',
    'Stoke City': 'Stoke',
    'Nottingham Forest': 'Nottingham',
    'Birmingham City': 'Birmingham',
    'Coventry City': 'Coventry',
    'Wimborne Town': 'Wimborne',
    'Llanelli Town': 'Llanelli',
    'King\'s Lynn Town': 'King\'s Lynn Town',
    'Blackburn Rovers': 'Blackburn',
    'Northampton Town': 'Northampton',
    'Newcastle': 'Newcastle United',
    'Beaconsfield Town': 'Beaconsfield',
    'Chemelil': 'Chemelil',
    'Sporting Braga': 'Sporting Braga',
    'Estoril': 'Estoril Praia',
    'Nacional': 'Nacional de Madeira',
    'Nzoia United': 'Nzoia Sugar',
    'Vitória Guimarães II': 'Vitória Guimarães II',
    'Marítimo': 'Maritimo',
    'Newcastle Jets': 'Newcastle Jets',
    'Vitória Setúbal': 'Vitoria Setubal',
    'RSB Berkane': 'RS Berkane',
    'Paphos': 'Pafos',
    'Vitória Guimarães': 'Vitória Guimarães',
    'Sporting Covilhã': 'Sporting Covilhã',
    'Met. Police FC': 'Met. Police FC',
    'Sporting Braga II': 'Sporting Braga II',
    'Homeboyz': 'Kakamega Homeboyz',
    'Raja Casablanca': 'Raja Casablanca Athletic',
    'SoNy Sugar': 'Sony Sugar',
    'AFC Bournemouth': 'Bournemouth',
    'KCB': 'KCB',
    'Famalicão': 'Famalicao',
    'WS Wanderers U21': 'Western Sydney Wanderers U21',
    'São Carlos U20': 'Sao Carlos Sp U20',
    'Criciuma U20': 'Criciúma U20',
    'Desportivo Aves': 'CD Aves',
    'Mirassol U20': 'Mirassol Futebol Clube U20',
    'Ríver U20': 'River-PI U20',
    'Confiança U20': 'Confianca U20',
    'El Gounah': 'El Gouna',
    'Flamengo RJ U20': 'Flamengo RJ U20',
    'Boavista U20': 'Boavista RJ U20',
    'Moreirense': 'Moreirense',
    'Rio Ave': 'Rio Ave',
    'Goias U20': 'Goias U20',
    'São Bento U20': 'São Bento U20',
    'Flamengo RJ U20': 'Flamengo RJ U20',
    'Ricanato U20': 'Ricanato U20',
    'Shillong Lajong': 'Lajong',
    'Hapoel Iksal': 'Hapoel Iksal Amad',
    'Chennai City': 'Chennai City',
    'Connah\'s Quay': 'Connahs Quay',
    'TNS': 'TNS',
    'Newcastle Utd U23': 'Newcastle United U23',
    'Chippa United': 'Chippa United',
    'Leganés': 'Leganes',
    'Al Ahly': 'Al Ahly Cairo',
    'Bloemfontein Celtic': 'Bloemfontein Celtic',
    'Pyramids FC': 'Pyramids',
    'Sektzia Nes Tziona': 'Sectzya Nes Ziona',
    'Hapoel Kfar-Saba': 'Hapoel Kfar Saba',
    'Gokulam': 'Gokulam',
    'The New Saints': 'New Saints',
    'CA Bordj Bou Arreridj': 'Bordj Bou Arreridj'
}


def scrapesite():

    # open website
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(chromedriver_path, options=options)
    #driver.get('http://www.google.com/xhtml')

    time.sleep(1)  # Let the user actually see something!

    driver.get("https://www.flashscore.com/football/")

    table_main = driver.find_element_by_class_name('table-main')
    soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

    table = soup.prettify()

    f = open('text.txt', 'w', encoding='utf-8')
    f.write(table)
    f.close()

    driver.quit()


def scrape777sport():

    # open website
    options = Options()
    #options.headless = True

    driver = webdriver.Chrome(chromedriver_path, options=options)

    time.sleep(1)  # Let the user actually see something!

    driver.get("https://777score.com")

    table_main = driver.find_element_by_class_name('main-table')
    soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

    table = soup.prettify()

    f = open('html777sport.txt', 'w', encoding='utf-8')
    f.write(table)
    f.close()

    driver.quit()


def extractlivescores777():

    global allgamesdf

    f = open('html777sport.txt', 'r', encoding='utf-8')
    lines = f.read().replace('\n', '')

    soup = BeautifulSoup(lines, 'html.parser')

    cols = ['progress', 'timer', 'time_of_match', 'team_home', 'team_away', 'score', 'hgoals', 'ggoals', 'hthgoals', 'htggoals', 'match_id',
            '777url']
    allgamesdf = pd.DataFrame(columns=cols)

    for span in soup.findAll("span", {"class": 'row'}):

        links = span.findAll('a', href=True)
        for link in links:
            l = link['href']
            #print(link['href'])
            gamesrow = []
            status = link.find("span", {"class": lambda x: x and "status" in x.split()})
            #print(status)
            timer = status.text.replace('\'','').replace('+','').strip()

            progress = ''
            if timer == 'Finished':
                progress = 'finished'
            elif timer == '':
                progress = 'scheduled'
            else: progress = 'live'

            gamesrow.append(progress)

            if timer in ['Halftime', '45+', 'Finished', 'Postponed','']:
                timer = 0
            gamesrow.append(timer)

            kick_off = link.find("span", {"class": 'date-time'})
            gamesrow.append(kick_off.text.strip())

            spans = link.findAll("span", {"class": 'team'})

            for c,v in enumerate(spans):
                gamesrow.append(v.find("span").text.strip())
            #print(teams)

            lives = link.findAll("span", {"class": lambda x: x and "score" in x.split()})
            #print(lives)
            for live in lives:
                scorespans = live.findAll("span")
                #print(live)
                hgoals = scorespans[0].text.strip().replace('-','')
                ggoals = scorespans[2].text.strip().replace('-','')
                if hgoals != '': score = (hgoals + ' - ' + ggoals)
                else: score = ''

                gamesrow.append(score)
                gamesrow.append(hgoals)
                gamesrow.append(ggoals)
                gamesrow.append('')
                gamesrow.append('')

        match_id = l.split('-')[-1]
        gamesrow.append(match_id)
        gamesrow.append(l)
        #print(gamesrow)

        allgamesdf = allgamesdf.append(pd.DataFrame([gamesrow], columns=cols), ignore_index=True)

        #print('\n' )

    allgamesdf.sort_values('time_of_match', inplace=True)
    allgamesdf.to_csv(path + 'allgames.csv', index=False)


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
                        hthgoals = 0
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

    allgamesdf.loc[allgamesdf['timer'].isin(['Half Time', '45+', 'Finished','Postponed']),'timer'] = 0
    allgamesdf['timer'] = allgamesdf['timer'].str.extract('(\d+)')#.astype(int)
    allgamesdf['timer'] = allgamesdf['timer'].infer_objects().fillna(0)
    allgamesdf.sort_values('time_of_match', inplace=True)
    allgamesdf.to_csv(path + 'allgames.csv', index=False)

    msg = 'There are {} games live'.format(len(allgamesdf))
    # TwitterMsg.sendDM(userids=userids, msg=msg)
    #Telegram().send_message(chat_id=localsettings.telegram_token, text=msg)


def addwatchlistinfo():

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    global allgamesdf

    values = {'fhg': '', 'shg': ''}
    try:
        watchlistfhg = pd.read_csv(path + 'watchlistfhg.csv')
        watchlistfhg.rename(str.lower, axis='columns', inplace=True)

        watchlistfhg['kick off'] = pd.to_datetime(watchlistfhg['kick off']).dt.date

        watchlistfhg = watchlistfhg[watchlistfhg['kick off'] == datetime.datetime.today().date()]

        watchlistfhg.rename(index=str, columns={'fhg' : 'fhg_perc'}, inplace=True)
        watchlistfhg['fhg'] = 'x'
        watchlistfhg['fixture'] = watchlistfhg['fixture'].str.replace(r'\([^)]*\)', '').str.strip()
    except Exception as e:
        print(e)
        print('watchlistfhg.csv not correct')
        c = ['fixture','competition','kick off','shg','shg_perc']
        watchlistfhg = pd.DataFrame(columns=c)

    try:
        watchlistshg = pd.read_csv(path + 'watchlistshg.csv')
        watchlistshg.rename(str.lower, axis='columns', inplace=True)
        watchlistshg.rename(index=str, columns={'shg' : 'shg_perc'}, inplace=True)

        watchlistshg['kick off'] = pd.to_datetime(watchlistshg['kick off']).dt.date

        watchlistshg = watchlistshg[watchlistshg['kick off'] == datetime.datetime.today().date()]

        watchlistshg.rename(index=str, columns={'shg' : 'shg_perc'}, inplace=True)
        watchlistshg['shg'] = 'x'
        watchlistshg['fixture'] = watchlistshg['fixture'].str.replace(r'\([^)]*\)', '').str.strip()

    except Exception as e:
        print(e)
        print('watchlistshg.csv not correct')
        c = ['fixture','competition','kick off','shg','shg_perc']
        watchlistshg = pd.DataFrame(columns=c)

    watchlist = watchlistfhg.merge(watchlistshg, how='outer', on=['fixture', 'competition'])

    watchlist['team_home'], watchlist['team_away'] = watchlist['fixture'].str.split(' vs. ', 1).str
    watchlist['team_home'] = watchlist['team_home'].str.strip().replace(teamnames)
    watchlist['team_away'] = watchlist['team_away'].str.strip().replace(teamnames)

    watchlist = watchlist[["team_home","team_away","fhg","shg","fhg_perc","shg_perc"]].fillna(value= values)
    watchlist.to_csv(path + 'watchlistnew.csv', index=False)

    # find non-matched games
    awaydiff = set(watchlist['team_away']).difference(set(allgamesdf['team_away']))
    homediff = set(watchlist['team_home']).difference(set(allgamesdf['team_home']))

    d = ['\'' + x + '\': \'' + x + '\','  for x in awaydiff.union(homediff)]
    if d:
        print('Check the names of the following teams in all games from flashscore')
        for k in d:
            print(k)

    allgamesdf = allgamesdf.merge(watchlist, on=['team_home','team_away'], how='left')

    oddsportalurls = pd.read_csv(path + 'matches/liveodds/oddsportalurls.csv')

    pmodds = pd.read_csv(path + 'matches/pmodds/pmodds.csv')

    allgamesdf = allgamesdf.merge(oddsportalurls, on='match_id', how='left')
    allgamesdf = allgamesdf.merge(pmodds, on=['team_home','team_away'], how='left')

    allgamesdf.to_csv(path + 'allgames.csv', index=False)


def addflagsandfields():
    global allgamesdf

    #   ___            __   __    ___  ___  __
    #  |__   /\  \  / /  \ |__) |  |  |__  /__`
    #  |    /~~\  \/  \__/ |  \ |  |  |___ .__/
    #

    allgamesdf["pmodd1"] = pd.to_numeric(allgamesdf.pmodd1, errors='coerce').astype(float)
    allgamesdf["pmodd2"] = pd.to_numeric(allgamesdf.pmodd2, errors='coerce').astype(float)

    allgamesdf.loc[(allgamesdf['pmodd1'] < 2.4) & (1.5 < allgamesdf['pmodd1']),'fav_home'] = 'x'
    allgamesdf.loc[(allgamesdf['pmodd2'] < 2.4) & (1.5 < allgamesdf['pmodd2']),'fav_away'] = 'x'

    allgamesdf.to_csv(path + 'allgames.csv', index=False)


def findlateshg():
    livegames = allgamesdf[(allgamesdf['progress'] == 'live')]
    lategames = livegames[(livegames['timer'].astype(int) > 70)]
    shg_watch = lategames[lategames['shg'] == 'x']

    if not lategames.empty:
        print('###################################')
        print('#            Late SHG             #')
        print('###################################')

        msg_list_title = '###### SHG from List Alert #######\n'
        msg_late00_title = '###### SH 0-0 Alert #######\n'

        for index, row in lategames.iterrows():
            summary = 'Reached {}\' in {} - {} at {}-{}'.format(row['timer'],row['team_home'],row['team_away'],row['hgoals'],row['ggoals']) + '\n' + \
                    'Check stats at https://777score.com/{}\n'.format(row['777url'])

            print('{}\' {}-{} ({}-{}) {} - {}  '.format(row['timer'],row['hgoals'],row['ggoals'],row['hthgoals'],row['htggoals'],row['team_home'],row['team_away']))

            if row['shg'] == 'x' and row['hgoals'] == row['hthgoals'] and row['ggoals'] == row['htggoals']:
                msg_list = msg_list_title + summary
                #TwitterMsg().senddm(userids=userids_list, msg=(row['match_id'], "SHG_list", msg_list))
                Telegram().send_message(chat_id=telegram_chat_id, msg=(row['match_id'], "SHG_list", msg_list))

            elif row['hgoals'] == '0' and row['ggoals'] == '0':
                msg_late00 = msg_late00_title + summary
                #TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "SHG", msg_late00))
                Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "SHG", msg_late00))
    else:
        print("no SHG candidates \n")


def findfhg():

    livefhgames = allgamesdf[(allgamesdf['progress'] == 'live') & (allgamesdf['timer'].astype(int) < 46)]
    print('\n{} live FH games found'.format(len(livefhgames)))

    latefhgames = livefhgames[(livefhgames['timer'].astype(int) > 30)]
    fhg_watch = latefhgames[latefhgames['fhg'] == 'x']

    if not latefhgames.empty:
        print('###################################')
        print('#           Late FHG              #')
        print('###################################')

        msg_list_title = '# FHG from List Alert #\n'
        msg_late00_title = '# FH still 0-0 Alert #\n'

        for index, row in latefhgames.iterrows():
            summary = 'Reached {}\' in {} - {} at {}-{}'.format(row['timer'],row['team_home'],row['team_away'],row['hgoals'],row['ggoals']) + '\n' + \
                    'Check stats at https://777score.com/{}\n'.format(row['777url'])

            print('{}\' {}-{} {} - {}  '.format(row['timer'],row['hgoals'],row['ggoals'],row['team_home'],row['team_away']))

            if row['fhg'] == 'x' and row['hgoals'] == '0' and row['ggoals'] == '0':
                msg_list = msg_list_title + summary
                #TwitterMsg().senddm(userids=userids_list, msg=(row['match_id'], "FHG_list", msg_list))
                Telegram().send_message(chat_id=telegram_chat_id, msg=(row['match_id'], "FHG_list", msg_list))

            elif row['hgoals'] == '0' and row['ggoals'] == '0':
                msg_late00 = msg_late00_title + summary
                #TwitterMsg().senddm(userids=userids, msg=(row['match_id'], "FHG", msg_late00))
                #Telegram().send_message(chat_id=telegram_chat_id, msg=(row['match_id'], "FHG", msg_late00))

    else:
        print("no FHG candidates \n")


def findgoodbet():
    findfavoritesbeforeht()


def findfavoritesbeforeht():

    livefhgames = allgamesdf[(allgamesdf['progress'] == 'live')]
    print('\n{} live FH games found'.format(len(livefhgames)))

    msg_title = '# Favorites fell behind  #\n'

    for index, row in livefhgames.iterrows():

        summary = 'Reached {}\' in {} - {} at {}-{}'.format(row['timer'], row['team_home'], row['team_away'],
                                                                 row['hgoals'], row['ggoals']) + '\n' + \
                  'Check stats at https://777score.com/{}\n'.format(row['777url'])

        if (row['fav_home'] == 'x' and row['hgoals'] < row['ggoals']) or (row['fav_away'] == 'x' and row['hgoals'] > row['ggoals']):
            msg_favbefht = msg_title + summary + '\nodds: {} - {}'.format(row['pmodd1'],row['pmodd2'])
            Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "FHG", msg_favbefht))

    msg_title = '# Favorites not ahead before HT #\n'

    for index, row in livefhgames.iterrows():

        summary = 'Reached {}\' in {} - {} at {}-{}'.format(row['timer'], row['team_home'], row['team_away'],
                                                                 row['hgoals'], row['ggoals']) + '\n' + \
                  'Check stats at https://777score.com/{}\n'.format(row['777url'])

        if (30 < int(row['timer']) < 46) and ((row['fav_home'] == 'x' and row['hgoals'] <= row['ggoals']) or (row['fav_away'] == 'x' and row['hgoals'] >= row['ggoals'])):
            msg_favnotaheadbfht = msg_title + summary + '\nodds: {} - {}'.format(row['pmodd1'],row['pmodd2'])
            Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "FHG", msg_favnotaheadbfht))


def dumpmatchsummary():

    games = pd.read_csv(path + 'allgames.csv')

    # open website
    options = Options()
    #options.headless = True

    driver = webdriver.Chrome(chromedriver_path, options=options)

    time.sleep(1) # Let the user actually see something!

    for index, row in games.iterrows():
        match_id = row['match_id']
        urlmatch = row['777url']

        if row['progress'] == 'live':

            exists = os.path.isfile(path + '/matches/pmodds/html/{}.txt'.format(match_id))

            if not exists:
                url = 'https://777score.com/{}'.format(urlmatch)
                print('getting {}'.format(url))

                driver.get(url)

                wait = WebDriverWait(driver, 5)
                f = open(path + 'matches/pmodds/html/{}.txt'.format(match_id), 'w', encoding='utf-8')

                try:
                    driver.find_element_by_class_name('button').click()

                    table = ''
                    try:
                        table_main = driver.find_element_by_class_name('statistics')
                        soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

                        table = soup.prettify()
                        f.write(table)

                    except:
                        print('Cannot find odds_1x2 class in {}'.format(url))


                except Exception as e:
                    print(e)

                f.close()

            else:
                #print('file odds already exists {}'.format(match_id))
                pass

    driver.quit()


def extractstatsfrommatchfiles():
    import re
    import json

    directory = os.fsencode(path + 'matches/pmodds/html/')

    for file in os.listdir(directory):
        match_id = str.replace(str(file, 'utf-8'), '.txt', '')

        lines = open(directory + file).read().replace('\n', '')
        soup = BeautifulSoup(lines, 'html.parser')
        divs = soup.findAll("div", {"class": 'bar'})

        d = dict()
        d['match_id'] = match_id

        for bar in divs:
            #print(bar.text)
            infos = bar.findAll("div", {"class": 'info'})
            for info in infos:
                spans = info.findAll("span")
                #print('found {} spans'.format(len(spans)))
                #for span in spans:
                home_value, metric_raw, away_value = spans
                metric = re.sub(' +', ' ', metric_raw.text.strip())
                d[metric] = {'home':re.sub(' +', ' ', home_value.text.replace('%','').strip()),
                             'away':re.sub(' +', ' ', away_value.text.replace('%','').strip())}

                #print(re.sub(' +', ' ', home_value.text), metric, re.sub(' +', ' ', away_value.text))


        with open(path + 'matches/pmodds/json/{}.json'.format(match_id), 'w') as fp:
            json.dump(d, fp, indent=2)


def scrapepmodds():

    filename = 'pmodds.csv'

    exists = os.path.isfile(path + '/matches/pmodds/{}'.format(filename))

    if not exists:
        # open website
        options = Options()
        #options.headless = True

        driver = webdriver.Chrome(chromedriver_path, options=options)

        driver.get("https://www.flashscore.com/football/")

        wait = WebDriverWait(driver, 5)

        live_games_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Odds")))
        live_games_link.click()

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "odds-format")))

        oddscols = ['team_home','team_away','pmodd1','pmoddx','pmodd2']
        oddsdf = pd.DataFrame(columns=oddscols)

        table_main = driver.find_elements_by_css_selector(".soccer.odds")
        for t in table_main:
            table = BeautifulSoup(t.get_attribute('innerHTML'), "html.parser")
            nation = str.replace(table.find("span", {"class": 'country_part'}).text, ':', '')
            league = table.find("span", {"class": 'tournament_part'}).text

            trs_live = table.findAll("tr", {"class": lambda x: x and "stage-live" in x.split()})
            trs_finished = table.findAll("tr", {"class": lambda x: x and "stage-finished" in x.split()})
            trs_scheduled = table.findAll("tr", {"class": lambda x: x and "stage-scheduled" in x.split()})

            trs = trs_live + trs_finished + trs_scheduled

            # print('found {} trs for {}: '.format(len(trs), nation))

            for index, tr in enumerate(trs):

                classes = tr.get('class')

                if 'stage-scheduled' in classes:

                    match_id = tr.get('id').split('_')[-1]

                    time_of_match = tr.find("td", {"class": lambda x: x and "time" in x.split()}).text
                    team_home = tr.find("td", {"class": lambda x: x and "team-home" in x.split()}).text
                    team_away = tr.find("td", {"class": lambda x: x and "team-away" in x.split()}).text

                    pmodd1 = tr.find("td", {"class": lambda x: x and "cell_oa" in x.split()}).text
                    pmoddx = tr.find("td", {"class": lambda x: x and "cell_ob" in x.split()}).text
                    pmodd2 = tr.find("td", {"class": lambda x: x and "cell_oc" in x.split()}).text
                    #print('{} - {} 1: {} - X: {} - 2: {} - {}'.format(team_home,team_away,odd1,oddx,odd2,match_id))

                    row = list(map(str.strip,[team_home, team_away, pmodd1, pmoddx, pmodd2]))
                    if pmodd1 != '-':
                        oddsdf = oddsdf.append(pd.DataFrame([row], columns=oddscols), ignore_index=True)

            oddsdf['team_home'] = oddsdf['team_home'].str.strip().replace(teamnames)
            oddsdf['team_away'] = oddsdf['team_away'].str.strip().replace(teamnames)
            oddsdf.to_csv(path + 'matches/pmodds/pmodds.csv', index=False)

        driver.quit()


def scrapeoddsportalurls():

    filename = 'oddsportalurls.csv'

    exists = os.path.isfile(path + '/matches/liveodds/{}'.format(filename))

    if not exists:

        cols = ['match_id', 'oddsportalurl']
        oddsportalurldf = pd.DataFrame(columns=cols)

        # open website
        options = Options()
        options.headless = True

        driver = webdriver.Chrome(chromedriver_path, options=options)
        driver.get("https://www.oddsportal.com/matches/soccer")

        table_main = driver.find_element_by_class_name('table-main')
        table = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

        tds = table.findAll("td", {"class": lambda x: x and "table-participant" in x.split()})
        for td in tds:
            links = td.findAll('a', href=True)
            for link in links:
                if link['href'] not in ['javascript:void(0);'] and 'inplay-odds' not in link['href']:
                    match_id = link['href'].rsplit('-', 1)[-1][:-1]
                    oddsportalurl = link['href']

                    row = list(map(str.strip, [match_id, oddsportalurl]))
                    oddsportalurldf = oddsportalurldf.append(pd.DataFrame([row], columns=cols), ignore_index=True)

        oddsportalurldf.to_csv(path +'/matches/liveodds/{}'.format(filename), index=False)
        driver.quit()


userids_list = ['442751368']# ['1208132010', '442751368']
userids = ['442751368']

scrapepmodds()
scrapeoddsportalurls()

scrape777sport()
extractlivescores777()

#scrapesite()
#extractlivescores()
addwatchlistinfo()
addflagsandfields()
#
findlateshg()
findfhg()
findgoodbet()

dumpmatchsummary()
extractstatsfrommatchfiles()
