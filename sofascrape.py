from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os
import glob
import datetime
import pandas as pd
import numpy as np

from localsettings import *

today = datetime.datetime.today().strftime('%Y%m%d')
tomorrow_sofa = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')


def scrapesofascorelive(sport ='football'):
    from selenium.webdriver import DesiredCapabilities

    # open website
    options = Options()
    #options.headless = True

    driver = webdriver.Chrome(chromedriver_path, options=options)
    #driver = webdriver.PhantomJS(executable_path=phantomjs_path)

    driver.get("https://www.sofascore.com/{}/livescore".format(sport))


    try:

        ep = ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'js-event-list-table-container')]"))
        WebDriverWait(driver, 10).until(ep)

        table_main = driver.find_element_by_xpath("//div[contains(@class, 'js-event-list-table-container')]")
        soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")
        #soup = BeautifulSoup(driver.page_source)

        table = soup.prettify()

        livefilename = path + 'html/{}/htmlsofascore_live_{}_{}.txt'.format(sport,today,sport)
        os.makedirs(os.path.dirname(livefilename), exist_ok=True)

        f = open(livefilename, 'w', encoding='utf-8')
        f.write(table)
        f.close()

        existstoday = os.path.isfile(path + 'html/{}/htmlsofascore_all_{}_{}.txt'.format(sport,today,sport))
        existstomorrow = os.path.isfile(path + 'html/{}/htmlsofascore_all_{}_{}.txt'.format(sport,tomorrow,sport))

        if datetime.datetime.today().hour >= 1 and not existstoday:
            driver.get("https://www.sofascore.com/{}".format(sport))

            ep = ec.presence_of_element_located((By.XPATH,"//div[contains(@class, 'js-event-list-table-container')]"))
            WebDriverWait(driver, 10).until(ep)

            table_main = driver.find_element_by_xpath("//div[contains(@class, 'js-event-list-table-container')]")
            soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

            table = soup.prettify()

            f = open(path + 'html/{}/htmlsofascore_all_{}_{}.txt'.format(sport,today,sport), 'w', encoding='utf-8')
            f.write(table)
            f.close()

        if not existstomorrow:
            driver.get("https://www.sofascore.com/{}/{}".format(sport,tomorrow_sofa))

            ep = ec.presence_of_element_located((By.XPATH,"//div[contains(@class, 'js-event-list-table-container')]"))
            WebDriverWait(driver, 10).until(ep)

            table_main = driver.find_element_by_xpath("//div[contains(@class, 'js-event-list-table-container')]")
            soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")

            table = soup.prettify()

            f = open(path + 'html/{}/htmlsofascore_all_{}_{}.txt'.format(sport,tomorrow.replace('-',''), sport), 'w', encoding='utf-8')
            f.write(table)
            f.close()

        driver.quit()

    except Exception as e:
        print(e)


def extractsofamatchlinks(sport = 'football', date=today):

    try:
        f = open(path + 'html/{}/htmlsofascore_live_{}_{}.txt'.format(sport,date,sport), 'r', encoding='utf-8')
        lines = f.read().replace('\n', '')

        soup = BeautifulSoup(lines, 'html.parser')

        links = soup.findAll("a", {"class": lambda x: x and "cell--event-list" in x.split()})

        f = open(path + 'matches/matchlinks/sofamatchlinks_live_{}_{}.txt'.format(date,sport), 'w', encoding='utf-8')

        for link in links:
            # print(link['href'])
            f.write('http://www.sofascore.com' + link['href'] + '\n')

        f.close()

    except Exception as e:
        print(e)

    try:
        f = open(path + 'html/{}/htmlsofascore_all_{}_{}.txt'.format(sport,date,sport), 'r', encoding='utf-8')
        lines = f.read().replace('\n', '')

        soup = BeautifulSoup(lines, 'html.parser')

        links = soup.findAll("a", {"class": lambda x: x and "cell--event-list" in x.split()})

        f = open(path + 'matches/matchlinks/sofamatchlinks_all_{}_{}.txt'.format(date,sport), 'w', encoding='utf-8')

        for link in links:
            # print(link['href'])
            f.write('http://www.sofascore.com' + link['href'] + '\n')

        f.close()

    except Exception as e:
        print(e)


def extractsofamatches(sport='football', date=today):

    import time

    from urllib.parse import urlparse
    from selenium.webdriver.common.action_chains import ActionChains

    #driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chromedriver_path, chrome_options=options)

    for infix in ['all','live']:
        print('Fetching {} games'.format(infix))

        try:
            pad = path + 'matches/matchlinks/sofamatchlinks_{}_{}_{}.txt'.format(infix, date, sport)
            f = open(pad, 'r', encoding='utf-8')

            for line in (x.strip() for x in f):
                filename = path + 'matches/sofamatch/{}/{}/{}.txt'.format(date,sport,urlparse(line)[2][1:])

                try:
                    stamp = datetime.datetime.fromtimestamp(os.path.getmtime(filename))

                    now = datetime.datetime.now()
                    ageoffile = divmod((now - stamp).total_seconds(), 3600)[0]
                except:
                    ageoffile = 5

                if ageoffile > 4 or infix == 'live':

                    try:
                        print('Getting {} - {}'.format(line,date))
                        driver.get(line)

                        if infix ==  'all':
                            xpad = '//*[@id="pjax-container-main"]/div/div[2]/div/div[1]/div[10]/div/div/div/div[1]/div/button'

                            w3 =driver.find_element_by_xpath('//button[starts-with(@data-vote,"1")]')
                            #btn = driver.find_element_by_xpath(xpad)
                            w3.click()
                            print('pressed button')
                            driver.implicitly_wait(2)

                            wait = WebDriverWait(driver, 10)
                            men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'vote__pct')]")))
                            ActionChains(driver).move_to_element(men_menu).perform()

                    except Exception as e:
                        print(e)

                    table_main = driver.find_element_by_class_name('page-container')
                    soup = BeautifulSoup(table_main.get_attribute('innerHTML'), "html.parser")
                    table = soup.prettify()


                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "w") as f:
                        print('File written')
                        f.write(table)
                        f.close()

        except Exception as e:
            print(e)

    driver.quit()


def statsfromsofafiles(sport='football',date=today):
    print('Extracting stats from sofafiles for {} at {}'.format(date,sport))

    allgames = [l.replace('http://www.sofascore.com/','').replace('\n','') + '.txt' for l in open(path + 'matches/matchlinks/sofamatchlinks_all_{}_{}.txt'.format(date, sport)).readlines()]
    try:
        livegames = [l.replace('http://www.sofascore.com/','').replace('\n','') + '.txt' for l in open(path + 'matches/matchlinks/sofamatchlinks_live_{}_{}.txt'.format(date, sport)).readlines()]
    except:
        livegames = []

    rootdir = os.fsencode(path + 'matches/sofamatch/{}/{}'.format(date,sport))

    # Votes
    if sport in ['football', 'handball', 'rugby']:
        colsvotes = ['match', 'voteperc_home', 'voteperc_draw', 'voteperc_away', 'islive']
    else:
        colsvotes = ['match', 'voteperc_home', 'voteperc_away', 'islive']
    votesdf = pd.DataFrame(columns=colsvotes)

    if len(allgames)>0:

        allgamesdf = pd.DataFrame(allgames)
        allgamesdf.columns = ['match']

        # Gameinfo
        colsgameinfo = ['match','timer','starttime']
        gameinfodf = pd.DataFrame(columns=colsgameinfo)

        for subdir, dirs, files in os.walk(rootdir):

            for file in files:
                ff = subdir.decode("utf-8").split('/')[-1] + '/' + file.decode("utf-8")

                print(b'stats from ' + os.path.join(subdir, file))
                lines = open(os.path.join(subdir, file)).read().replace('\n', '')
                soup = BeautifulSoup(lines, 'html.parser')


                timerdict = {
                    'Halftime':45
                }
                # game information
                try:
                    gameinforow = [ff]
                    timer = soup.find("span", {"class": lambda x: x and "js-event-widget-header-timer-container" in x.split()})
                    t = timer.text.strip()
                    tt = timerdict.get(t, t)
                    gameinforow.append(tt)
                except:
                    gameinforow.append('unknown')

                try:
                    starttime = soup.find("div", {"class": lambda x: x and "cell--start" in x.split()})
                    st = starttime.find("div", {"class": lambda x: x and "cell__content" in x.split()})
                    gameinforow.append(st.text.strip().replace('Today at ',''))
                except:
                    gameinforow.append('unknown')

                gameinfodf = gameinfodf.append(pd.DataFrame([gameinforow], columns=colsgameinfo), ignore_index=True)

                if t not in ['Ended','AET']:
                    # votes
                    gamesrow = [ff]

                    votesdiv = soup.find("div", {"class": 'js-vote-stats-container'})
                    if votesdiv:
                        voteperc = votesdiv.findAll("span", {"class": lambda x: x and "vote__pct" in x.split()})
                        perc_home = -1.0
                        perc_draw = -1.0
                        perc_away = -1.0
                        if len(voteperc) > 0 :
                            perc_home = floatOrZero(voteperc[0].text.strip().replace('%',''))
                            if sport in ['football', 'handball', 'rugby']:
                                perc_draw = floatOrZero(voteperc[1].text.strip().replace('%', ''))
                                perc_away = floatOrZero(voteperc[2].text.strip().replace('%',''))
                            else:
                                perc_away = floatOrZero(voteperc[1].text.strip().replace('%', ''))
                        gamesrow.append(perc_home)
                        if sport in ['football', 'handball', 'rugby']:
                            gamesrow.append(perc_draw)
                        gamesrow.append(perc_away)
                        if ff in livegames:
                            gamesrow.append('x')
                        else:
                            gamesrow.append('')

                        votesdf = votesdf.append(pd.DataFrame([gamesrow], columns=colsvotes), ignore_index=True)

        allgamesdf = allgamesdf.merge(gameinfodf,on="match",how='left')
        allgamesdf = allgamesdf.merge(votesdf,on="match",how='left')

        d = path + 'datafiles/{}/{}/'.format(date,sport)
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
    else:
        allgamesdf = pd.DataFrame([''])
        allgamesdf.columns = ['match']

    allgamesdf.to_csv(path + 'datafiles/{}/{}/allgamesvotes_{}_{}.csv'.format(date,sport,date,sport), index=False)


def getlivescores(sport='football',date=today):
    print('Getting live scores for {}'.format(sport))

    if sport in ['football']:
        cols = ['match', 'p1h', 'p1a']
    elif sport in ['basketball', 'handball', 'rugby', 'badminton', 'tennis']:
        cols = ['match', 'p1h', 'p2h', 'p3h', 'p4h', 'poth', 'p1a', 'p2a', 'p3a', 'p4a', 'pota']
    elif sport == 'volleyball':
        cols = ['match', 'p1h', 'p2h', 'p3h', 'p4h', 'p5h', 'p6h', 'p7h', 'p8h', 'p1a', 'p2a', 'p3a', 'p4a', 'p5a',
                'p6a', 'p7a', 'p8a']
    livescores = pd.DataFrame([], columns=cols)

    try:
        f = open(path + 'html/{}/htmlsofascore_live_{}_{}.txt'.format(sport,date,sport), 'r', encoding='utf-8')
        lines = f.read().replace('\n', '')

        soup = BeautifulSoup(lines, 'html.parser')

        links = soup.findAll("a", {"class": lambda x: x and "cell--event-list" in x.split()})

        for link in links:

            id = link['href'][1:] + '.txt'
            scores = [id]
            divs = link.findAll("div", {"class": lambda x: x and "event-rounds__final-score" in x.split()})
            for div in divs:
                scoredivs = div.findAll("div", {"class": lambda x: x and "cell__content" in x.split()})
                for div in scoredivs:
                    if div.text.strip().isdigit():
                        score = int(div.text.strip())
                    else: score = 0
                    scores.append(score)
                #if len(scores) > 10:
            scoredf = pd.DataFrame([scores], columns = cols)
            livescores = livescores.append(scoredf)
            print(scores)
    except Exception as e:
        print(e)

    livescores.to_csv(path + 'datafiles/{}/{}/livescores_{}_{}.csv'.format(date,sport,date,sport), index=False)


def mergeallframes(sport='football',date=today):
    print('Merging all frames for {} at {}'.format(date,sport))
    #allgamesdf = pd.read_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport))

    try:
        v = pd.read_csv(path + 'datafiles/{}/{}/allgamesvotes_{}_{}.csv'.format(date,sport,date,sport))
        o = pd.read_csv(path + 'matches/pmodds/oddsdf_{}_{}.csv'.format(date,sport))
        a = o.merge(v, on="match", how="outer")
        try: # if no livescores because tomorrow
            s = pd.read_csv(path + 'datafiles/{}/{}/livescores_{}_{}.csv'.format(date,sport,date,sport))
            ag = a.merge(s, on="match", how="left")
            ag.sort_values(by='timer', inplace=True)
        except:
            ag = a
        # create watchlist
        p = path + 'datafiles/{}/{}/watchlist_{}_{}.csv'.format(date,sport,date,sport)
        if not os.path.isfile(p):
            pp = ag.reindex(columns=['match'] + ['fhg','shg'])
            pp.to_csv(p, index=False)
        else:
            pp = pd.read_csv(p)

        ag['timer'] = ag['timer'].str.split('+').str[0].str.split(':').str[0]

        ag2 = ag.merge(pp, on="match", how="left")

        ag2.to_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport), index=False)

        ag2[ag2['islive'] == 'x'].to_csv(path + 'datafiles/{}/{}/livegames_{}_{}.csv'.format(date,sport,date,sport), index=False)

        if date == today:
            allgamesdf = ag

    except Exception as e:
        print('mergeallframes: ' + str(e))


def floatOrZero(value):
    try:
        return float(value)
    except:
        return 0.0


def extractpmodds(sport='football', date=today):
    print('Extracting PM odds for {} at {}'.format(date,sport))

    filename = 'oddsdf_{}_{}.csv'.format(date,sport)

    exists = os.path.isfile(path + '/matches/pmodds/{}'.format(filename))

    if not exists:

        allgames = [l.replace('http://www.sofascore.com/','').replace('\n','') + '.txt' for l in open(path + 'matches/matchlinks/sofamatchlinks_all_{}_{}.txt'.format(date,sport)).readlines()]
        if len(allgames) > 0:
            rootdir = os.fsencode(path + 'matches/sofamatch/{}/{}'.format(date,sport))

            oddsdf = pd.DataFrame(allgames)
            oddsdf.columns = ['match']

            # Votes
            if sport in ['football','handball','rugby']:
                cols = ['match', 'odds_home', 'odds_draw', 'odds_away']
            else:
                cols = ['match', 'odds_home', 'odds_away']
            oddsdf = pd.DataFrame(columns=cols)

            for subdir, dirs, files in os.walk(rootdir):

                for file in files:
                    ff = subdir.decode("utf-8").split('/')[-1] + '/' + file.decode("utf-8")
                    gamesrow = [ff]
                    print(b'odds from - ' + os.path.join(subdir, file))
                    lines = open(os.path.join(subdir, file)).read().replace('\n', '')

                    soup = BeautifulSoup(lines, 'html.parser')

                    oddlink = soup.findAll("span", {"class": lambda x: x and "u-fs18" in x.split()})
                    if oddlink:
                        print(b'found odds for ' + file)
                        for odd in oddlink:
                            o = odd.find("span", {"class": lambda x: x and "js-odds-value-decimal" in x.split()})
                            if o:
                                ot = o.text.strip()
                            else:
                                ot = 0

                            gamesrow.append(ot)

                        oddsdf = oddsdf.append(pd.DataFrame([gamesrow], columns=cols), ignore_index=True)
        else:
            oddsdf = pd.DataFrame(columns = ['match'])

        oddsdf.to_csv(path + '/matches/pmodds/{}'.format(filename), index=False)


def calculatestats(sport='football', date=today):
    print('Calculating stats for {} at {}'.format(date,sport))

    allgamesdf = pd.read_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport))

    try:
        allgamesdf['oddskew'] = round(100 / allgamesdf['voteperc_home'] / allgamesdf['odds_home'],2)
        allgamesdf['lt_home'] = round(allgamesdf['voteperc_home'] * allgamesdf['odds_home'] - 100,2)
        allgamesdf['lt_away'] = round(allgamesdf['voteperc_away'] * allgamesdf['odds_away'] - 100,2)

        allgamesdf['oddslead'] = np.where(
                        allgamesdf['odds_home'] > allgamesdf['odds_away']
                        , 'away'
                        , np.where(allgamesdf['odds_away'] > 0, 'home', 'none')
        )

        allgamesdf['votesabsdiff'] = round(abs(allgamesdf['voteperc_home'] - allgamesdf['voteperc_away']),2)
        allgamesdf['voteslead'] = np.where(
                        allgamesdf['voteperc_home'] > allgamesdf['voteperc_away']
                        , 'home'
                        , np.where(allgamesdf['voteperc_away'] > 0, 'away', 'none')
        )

        if sport in ['football']:
            hcolstosum = ['p1h']
            acolstosum = ['p1a']
        elif sport in ['basketball','handball','rugby','badminton','tennis']:
            hcolstosum = ['p1h','p2h','p3h','p4h','poth']
            acolstosum = ['p1a','p2a','p3a','p4a','pota']
        elif sport == 'volleyball':
            hcolstosum = ['p1h','p2h','p3h','p4h','p5h','p6h','p7h','p8h']
            acolstosum = ['p1a','p2a','p3a','p4a','p5a','p6a','p7a','p8a']

        if date==today:
            allgamesdf['ph'] = allgamesdf[hcolstosum].sum(axis=1)
            allgamesdf['pa'] = allgamesdf[acolstosum].sum(axis=1)
            allgamesdf['pabsdiff'] = abs(allgamesdf['ph'] - allgamesdf['pa'])
            allgamesdf['lead'] = np.where(
                                allgamesdf['ph'] > allgamesdf['pa']
                                , 'home'
                                , np.where(allgamesdf['pa'] > 0, 'away', 'none')
            )
        elif date==tomorrow:
            allgamesdf['ph'] = 0
            allgamesdf['pa'] = 0
            allgamesdf['pabsdiff'] = 0
            allgamesdf['lead'] = 'none'

        allgamesdf = allgamesdf[['match', 'odds_home', 'odds_away', 'starttime', 'timer',
         'voteperc_home', 'voteperc_away', 'lt_home', 'lt_away', 'islive', 'oddskew', 'oddslead',
         'votesabsdiff', 'voteslead', 'ph', 'pa', 'pabsdiff', 'lead', 'fhg', 'shg'] + hcolstosum + acolstosum]
        allgamesdf.to_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport), index=False)
        allgamesdf.to_html(path + 'datafiles/{}/{}/allgames_{}_{}.html'.format(date, sport, date, sport), index=False)
        allgamesdf[allgamesdf['islive'] == 'x'].to_csv(
            path + 'datafiles/{}/{}/livegames_{}_{}.csv'.format(date, sport, date, sport), index=False)

    except Exception as e:
        print('calculatestats: ' + str(e))