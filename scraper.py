#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        'AFC Bournemouth': 'Bournemouth',
        'AFC Hornchurch': 'Hornchurch',
        'AFC Rushden & Diamonds': 'AFC Rushden & Diamonds',
        'AFC Telford': 'Telford United',
        'Accrington Stanley': 'Accrington',
        'Ajman': 'Ajman',
        'Al Ahly': 'Al Ahly Cairo',
        'Al Dhafra': 'Al Dhafra',
        'Al Fujairah': 'Al Fujairah',
        'Al Ittifaq': 'Al-Ettifaq',
        'Al Ittihad': 'Al Ittihad',
        'Al Ittihad Kalba': 'Al Ittihad Kalba',
        'Al Jazira': 'Al Jazira',
        'Al Raed': 'Al-Raed',
        'Al Sharjah': 'Al Sharjah',
        'Al Wahda': 'Al Wahda',
        'Al Wasl': 'Al Wasl',
        'Alcorcón': 'Alcorcon',
        'Aldershot': 'Aldershot',
        'Aldershot Town': 'Aldershot',
        'Alki Oroklini': 'Alki Oroklini',
        'Altrincham': 'Altrincham',
        'AmaZulu': 'AmaZulu',
        'Anorthosis': 'Anorthosis',
        'Ashdod': 'Moadon Sport Ashdod',
        'Ashton United': 'Ashton Utd',
        'Athletic Club II': 'Athletic Club II',
        'Atlético San Luis': 'Atlético San Luis',
        'Aurrerá de Vitoria': 'Aurrerá de Vitoria',
        'Babaçu U20': 'CA Babacu U20',
        'Bala': 'Bala',
        'Bala Town': 'Bala',
        'Ballymena United': 'Ballymena',
        'Banbury United': 'Banbury',
        'Bani Yas': 'Bani Yas',
        'Barnet': 'Barnet',
        'Barry Town United': 'Barry Town',
        'Basingstoke': 'Basingstoke',
        'Basingstoke Town': 'Basingstoke',
        'Beaconsfield': 'Beaconsfield',
        'Beaconsfield Town': 'Beaconsfield',
        'Beitar Tel Aviv Ramla': 'Beitar Tel Aviv',
        'Benfica II': 'Benfica B',
        'Biggleswade Town': 'Biggleswade Town',
        'Birmingham City': 'Birmingham',
        'Blackburn Rovers': 'Blackburn',
        'Bloemfontein Celtic': 'Bloemfontein Celtic',
        'Boavista U20': 'Boavista RJ U20',
        'Boston United': 'Boston Utd',
        'Boston Utd': 'Boston Utd',
        'Bradford PA': 'Bradford PA',
        'Bradford Park Avenue': 'Bradford PA',
        'Braintree': 'Braintree',
        'Braintree Town': 'Braintree',
        'Brechin': 'Brechin',
        'Bright Stars': 'Bright Stars',
        'Brightlingsea Regent': 'Brightlingsea',
        'Burgess Hill': 'Burgess Hill',
        'Burgess Hill Town': 'Burgess Hill',
        'Burton': 'Burton',
        'CA Bordj Bou Arreridj': 'Bordj Bou Arreridj',
        'Caernarfon Town': 'Caernarfon Town',
        'Cape Town City': 'Cape Town City',
        'Cardiff MU': 'Cardiff MU',
        'Carmarthen Town': 'Carmarthen Town',
        'Chelmsford': 'Chelmsford',
        'Chelmsford City': 'Chelmsford',
        'Cheltenham': 'Cheltenham',
        'Cheltenham Town': 'Cheltenham',
        'Chemelil': 'Chemelil',
        'Chennai City': 'Chennai City',
        'Chesham': 'Chesham',
        'Chesham United': 'Chesham',
        'Chester': 'Chester',
        'Chippa United': 'Chippa United',
        'Ironi Kiryat Shmona': 'Ironi Kiryat Shmona',
        'Chippenham': 'Chippenham',
        'Chippenham Town': 'Chippenham',
        'Chorley': 'Chorley',
        'Churchill Brothers': 'Churchill Brothers',
        'Cimarrones de Sonora': 'Cimarrones',
        'Coalville': 'Coalville',
        'Coalville Town': 'Coalville',
        'Colchester': 'Colchester',
        'Colchester United': 'Colchester',
        'Confiança U20': 'Confianca U20',
        'Connah\'s Quay': 'Connahs Quay',
        'Corinthian-Casuals': 'Corinthian-Casuals',
        'Coventry': 'Coventry',
        'Coventry City': 'Coventry',
        'Crawley': 'Crawley',
        'Criciuma U20': 'Criciúma U20',
        'Cruz Azul': 'Cruz Azul',
        'Curzon Ashton': 'Curzon Ashton',
        'Deportivo Alavés': 'Alaves',
        'Derby County': 'Derby',
        'Desportivo Aves': 'CD Aves',
        'Dibba Al Fujairah': 'Dibba Al Fujairah',
        'Doncaster Rovers': 'Doncaster',
        'Dorchester': 'Dorchester',
        'Dorchester Town': 'Dorchester',
        'Dorking Wanderers': 'Dorking',
        'Druids': 'Druids',
        'Dundee Utd': 'Dundee Utd',
        'Dundee Utd.': 'Dundee Utd.',
        'Dungannon Swifts': 'Dungannon',
        'ES Metlaoui': 'Metlaoui',
        'East Thurrock': 'East Thurrock',
        'East Thurrock United': 'East Thurrock',
        'Eastbourne Boro': 'Eastbourne Boro',
        'Eastbourne Borough': 'Eastbourne Boro',
        'El Gounah': 'El Gouna',
        'Emirates': 'Emirates',
        'Estoril': 'Estoril Praia',
        'Exeter City': 'Exeter',
        'Extremadura UD': 'Extremadura UD',
        'FC United': 'FC United',
        'Famalicão': 'Famalicao',
        'Farnborough': 'Farnborough',
        'Farsley': 'Farsley',
        'Farsley Celtic': 'Farsley',
        'Ferroviário': 'Ferroviaria',
        'Fjölnir': 'Fjolnir',
        'Flamengo RJ U20': 'Flamengo RJ U20',
        'Fleetwood Town': 'Fleetwood',
        'Folkestone': 'Folkestone',
        'Folkestone Invicta': 'Folkestone',
        'Forest Green Rovers': 'Forest Green',
        'Fylde': 'AFC Fylde',
        'Gainsborough': 'Gainsborough',
        'Gainsborough Trinity': 'Gainsborough',
        'Goias U20': 'Goias U20',
        'Gokulam': 'Gokulam',
        'Gosport': 'Gosport',
        'Gosport Borough': 'Gosport',
        'Grimsby Town': 'Grimsby',
        'Halesowen': 'Halesowen',
        'Halesowen Town': 'Halesowen',
        'Halifax Town': 'Halifax Town',
        'Hamilton Academical': 'Hamilton',
        'Hampton & Richmond': 'Hampton & Richmond',
        'Hapoel Beer Sheva': 'H. Beer Sheva',
        'Hapoel Iksal': 'Hapoel Iksal Amad',
        'Hapoel Kfar-Saba': 'Hapoel Kfar Saba',
        'Hapoel Raanana': 'H. Raanana',
        'Hapoel Ramat HaSharon': 'Ramat Hasharon',
        'Haringey': 'Haringey',
        'Haringey Borough': 'Haringey',
        'Harrogate Town': 'Harrogate Town',
        'Hartley Wintney': 'Hartley Wintney',
        'Haverfordwest County': 'Haverfordwest County',
        'Hednesford': 'Hednesford',
        'Hendon': 'Hendon',
        'Hereford': 'Hereford',
        'Homeboyz': 'Kakamega Homeboyz',
        'Hull City': 'Hull',
        'Inverness CT': 'Inverness',
        'Ironi Kiryat Shmona': 'Hapoel Kiryat Shmona',
        'KCB': 'KCB',
        'King\'s Lynn Town': 'King\'s Lynn Town',
        'Kings Langley': 'Kings Langley',
        'Kirinya Jinja SS': 'Jinja',
        'Lancaster': 'Lancaster',
        'Lancaster City': 'Lancaster',
        'Langreo': 'Langreo',
        'Leatherhead': 'Leatherhead',
        'Leeds United': 'Leeds',
        'Leganés': 'Leganes',
        'Leicester City': 'Leicester',
        'Leiknir Reykjavík': 'Leiknir Reykjavik',
        'Leioa': 'Leioa',
        'Leiston': 'Leiston',
        'Llanelli Town': 'Llanelli',
        'Lowestoft': 'Lowestoft',
        'Lowestoft Town': 'Lowestoft',
        'Luton': 'Luton',
        'MacaÃ©': 'Macae',
        'Maccabi Netanya': 'Netanya',
        'Macclesfield': 'Macclesfield',
        'Macclesfield Town': 'Macclesfield',
        'Man Utd': 'Manchester Utd',
        'Mansfield': 'Mansfield',
        'Mansfield Town': 'Mansfield',
        'Margate': 'Margate',
        'Marine': 'Marine',
        'Marília U20': 'Marilia Sp U20',
        'Marítimo': 'Maritimo',
        'Matlock': 'Matlock',
        'Matlock Town': 'Matlock',
        'Merstham': 'Merstham',
        'Merstham (16)': 'Merstham',
        'Merthyr T': 'Merthyr T',
        'Merthyr Town': 'Merthyr T',
        'Met. Police FC': 'Met. Police FC',
        'Metropolitan Police FC': 'Met. Police FC',
        'Mickleover Sports': 'Mickleover Sports',
        'Mineros de Zacatecas': 'Mineros de Zacatecas',
        'Minerva Punjab': 'Minerva Punjab FC',
        'Mirassol U20': 'Mirassol Futebol Clube U20',
        'Moreirense': 'Moreirense',
        'Morelia': 'Morelia',
        'Nacional': 'Nacional de Madeira',
        'Nantwich': 'Nantwich',
        'Nantwich Town': 'Nantwich',
        'Needham Market': 'Needham Market',
        'Newcastle': 'Newcastle United',
        'Newcastle Jets': 'Newcastle Jets',
        'Newcastle United': 'Newcastle',
        'Newcastle Utd U23': 'Newcastle United U23',
        'Newport Co': 'Newport Co',
        'Newport County': 'Newport Co',
        'Newry City AFC': 'Newry City',
        'North Ferriby': 'North Ferriby',
        'North Ferriby United': 'North Ferriby',
        'Northampton Town': 'Northampton',
        'Norwich City': 'Norwich',
        'Nottingham Forest': 'Nottingham',
        'Notts Co': 'Notts Co',
        'Notts County': 'Notts Co',
        'Nova Iguacu': 'Nova Iguacu',
        'Nuneaton': 'Nuneaton',
        'Nuneaton Town': 'Nuneaton',
        'Nzoia United': 'Nzoia Sugar',
        'Ohod Madinah': 'Ohod',
        'Oldham Athletic': 'Oldham',
        'Oxford City': 'Oxford City',
        'Oxford United': 'Oxford Utd',
        'Paphos': 'Pafos',
        'Paradou AC': 'Paradou',
        'Plymouth Argyle': 'Plymouth',
        'Polokwane City': 'Polokwane City',
        'Poole': 'Poole',
        'Poole Town': 'Poole',
        'Port Vale': 'Port Vale',
        'Porto II': 'Porto B',
        'Potters Bar': 'Potters Bar',
        'Potters Bar Town': 'Potters Bar',
        'Preston North End': 'Preston',
        'Puebla': 'Puebla',
        'Pyramids FC': 'Pyramids',
        'Queens Park Rangers': 'Queen\'s Park',
        'RSB Berkane': 'RS Berkane',
        'Racing Santander': 'Racing Santander',
        'Raja Casablanca': 'Raja Casablanca Athletic',
        'Real Kings': 'Real Kings',
        'Real Zaragoza': 'Real Zaragoza',
        'Redditch': 'Redditch',
        'Redditch United': 'Redditch',
        'Ricanato U20': 'Ricanato U20',
        'Rio Ave': 'Rio Ave',
        'Rotherham United': 'Rotherham',
        'Royston': 'Royston',
        'Royston Town': 'Royston',
        'Rushall': 'Rushall',
        'Rushall Olympic': 'Rushall',
        'Ríver U20': 'River-PI U20',
        'Salisbury': 'Salisbury',
        'Sektzia Nes Tziona': 'Sectzya Nes Ziona',
        'Shabab Al Ahli Dubai': 'Shabab Al Ahli Dubai',
        'Sheffield United': 'Sheffield Utd',
        'Sheffield Wed': 'Sheffield Wed',
        'Shillong Lajong': 'Lajong',
        'Shrewsbury Town': 'Shrewsbury',
        'Slough': 'Slough',
        'Slough Town': 'Slough',
        'SoNy Sugar': 'Sony Sugar',
        'South Shields': 'South Shields',
        'Southend United': 'Southend',
        'Southport': 'Southport',
        'Spennymoor': 'Spennymoor',
        'Sporting Braga': 'Sporting Braga',
        'Sporting Braga II': 'Sporting Braga II',
        'Sporting CP': 'Sporting',
        'Sporting Covilhã': 'Sporting Covilhã',
        'Sporting Gijon II': 'Sporting Gijon B',
        'Sporting Gijón': 'Sporting Gijón',
        'St Albans City': 'St. Albans',
        'St Ives Town': 'St. Ives',
        'St Neots Town': 'St. Neots',
        'St. Albans': 'St. Albans',
        'St. Ives': 'St. Ives',
        'St. Neots': 'St. Neots',
        'Stafford Rangers': 'Stafford Rangers',
        'Staines': 'Staines',
        'Staines Town': 'Staines',
        'Stalybridge': 'Stalybridge',
        'Stalybridge Celtic': 'Stalybridge',
        'Stockport': 'Stockport',
        'Stockport County': 'Stockport',
        'Stoke City': 'Stoke',
        'Stratford': 'Stratford',
        'SuperSport United': 'SuperSport United',
        'Swansea City': 'Swansea',
        'Swindon Supermarine': 'Swindon S',
        'São Bento U20': 'São Bento U20',
        'São Carlos U20': 'Sao Carlos Sp U20',
        'TNS': 'TNS',
        'Tampico Madero': 'Tampico Madero',
        'Tamworth': 'Tamworth',
        'The New Saints': 'New Saints',
        'Tiverton': 'Tiverton',
        'Tiverton Town': 'Tiverton',
        'Toluca': 'Toluca',
        'Torquay': 'Torquay',
        'Torquay United': 'Torquay',
        'Tottenham Hotspur': 'Tottenham',
        'Truro': 'Truro',
        'Truro City': 'Truro',
        'UD Logroñés': 'UD Logroñés',
        'Uganda Police FC': 'Police',
        'Uniclinic': 'Uniclinic',
        'United of Manchester': 'FC United',
        'University of Pretoria': 'University of Pretoria',
        'Venados': 'Venados',
        'Villarreal II': 'Villarreal B',
        'Vipers': 'Vipers',
        'Vitória Guimarães': 'Vitória Guimarães',
        'Vitória Guimarães II': 'Vitória Guimarães II',
        'Vitória Setúbal': 'Vitoria Setubal',
        'WS Wanderers U21': 'Western Sydney Wanderers U21',
        'WS Wanderers W': 'WS Wanderers W',
        'Walton Casuals': 'Walton Casuals',
        'Warrenpoint Town': 'Warrenpoint',
        'Warrington Town': 'Warrington Town',
        'West Bromwich Albion': 'West Brom',
        'Western Sydney Wanderers': 'Western Sydney',
        'Weston-super-Mare': 'Weston-super-Mare',
        'Weymouth': 'Weymouth',
        'Whitehawk': 'Whitehawk',
        'Wigan Athletic': 'Wigan',
        'Wimborne': 'Wimborne',
        'Wimborne Town': 'Wimborne',
        'Wingate & Finchley': 'Wingate & Finchley',
        'Witton': 'Witton',
        'Witton Albion': 'Witton',
        'Woking': 'Woking',
        'Workington': 'Workington',
        'Worthing': 'Worthing',
        'Wycombe Wanderers': 'Wycombe',
        'York': 'York',
        'York City': 'York',
        'Zamalek': 'Zamalek'
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
    from selenium.webdriver import DesiredCapabilities

    # open website
    options = Options()
    #options.headless = True

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    driver = webdriver.Chrome(chromedriver_path, options=options, desired_capabilities=capabilities)

    time.sleep(1)  # Let the user actually see something!

    driver.get("https://777score.com")

    wait = WebDriverWait(driver, 5)

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
            if timer in ['Finished','Finished AP']:
                progress = 'finished'
            elif timer == '':
                progress = 'scheduled'
            else: progress = 'live'

            gamesrow.append(progress)

            if timer in ['Halftime', '45+', 'Finished', 'Postponed','Finished AP','']:
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

    watchlist = watchlistfhg.merge(watchlistshg, how='outer', on=['kick off','fixture', 'competition'])

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
                    wait = WebDriverWait(driver, 5)

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

#for key in sorted(teamnames):
#    print("\'%s\': \'%s\'," % (key, teamnames[key]))
