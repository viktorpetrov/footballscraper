#!/usr/bin/python

import numpy as np

from sofascrape import *

global allgamesdf
global userids

today = datetime.datetime.today().strftime('%Y%m%d')


def floatOrZero(value):
    try:
        return float(value)
    except:
        return 0.0


def findfavoritestrailing(minpointsmargin=7, minvotesmargin=20, date=today):

    allgamesdf = pd.read_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport))

    try:
        favlosing = allgamesdf[(allgamesdf['lead'] != allgamesdf['voteslead'])
                               & (allgamesdf['pabsdiff'] >= minpointsmargin)
                                & (allgamesdf['votesabsdiff'] >= minvotesmargin)]

        for index, row in favlosing.iterrows():
            print('favorites losing in {} \n'
                  '{} leads by {} points \n'
                  'but odds were in favour of {} : {}'.format(row['match'], row['lead'], row['pabsdiff'], row['oddslead'], row['odds_home']))
    except:
        pass


def findprematchdiscrepancies(date=today):
    allgamesdf = pd.read_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport))

    try:
        prematch = allgamesdf[(allgamesdf['starttime'] != 'Ended') & (allgamesdf['starttime'] != 'AET')]
        suspects = prematch[(prematch['voteslead'] != prematch['oddslead']) & (prematch['voteslead'] != 'none') & (prematch['oddslead'] != 'none')]
        suspects.to_csv(path + 'datafiles/{}/{}/suspects_{}_{}.csv'.format(date,sport,date,sport), index=False)
    except:
        pass


def findvaluebets(date=today):
    allgamesdf = pd.read_csv(path + 'datafiles/{}/{}/allgames_{}_{}.csv'.format(date,sport,date,sport))

    try:
        prematch = allgamesdf[(allgamesdf['starttime'] != 'Ended') & (allgamesdf['starttime'] != 'AET')]
        suspectsvalue1 = prematch[(prematch['voteslead'] == prematch['oddslead']) & (prematch['voteslead'] != 'none') & (prematch['oddslead'] != 'none')]
        suspectsvalue2 = suspectsvalue1[(suspectsvalue1['odds_home'] > 1.7) & (suspectsvalue1['oddslead'] == 'home')]
        suspectsvalue2.to_csv(path + 'datafiles/{}/{}/suspectsvalue2_{}_{}.csv'.format(date,sport,date,sport), index=False)

        closecalls1 = prematch[prematch['votesabsdiff'] < 10]

        closecalls1.to_csv(path + 'datafiles/{}/{}/closecalls1_{}_{}.csv'.format(date,sport,date,sport), index=False)

        #oddsoff = allgamesdf[abs(allgamesdf['oddskew'] - 1) > 0.3]

        oddsoff_home = allgamesdf[(allgamesdf['lt_home'] > 10) & (allgamesdf['odds_home'] > 1.8)]
        oddsoff_away = allgamesdf[(allgamesdf['lt_away'] > 10) & (allgamesdf['odds_away'] > 1.8)]
        oddsoff = oddsoff_away.append(oddsoff_home)
        oddsoff.sort_values(by='lt_home', inplace=True)
        oddsoff.to_csv(path + 'datafiles/{}/{}/oddsoff_{}_{}.csv'.format(date,sport,date,sport), index=False)
    except:
        pass


tomorrow_only = False

for sport in ['basketball','rugby','handball','volleyball','football','tennis']:

    if not tomorrow_only:
        scrapesofascorelive(sport)
        extractsofamatchlinks(sport)
        extractsofamatches(sport)
        extractpmodds(sport=sport)
        statsfromsofafiles(sport=sport)

        getlivescores(sport=sport)
        mergeallframes(sport=sport)

        calculatestats(sport=sport)
        findfavoritestrailing()
        findprematchdiscrepancies()
        findvaluebets()

    if datetime.datetime.today().hour >= 15 and tomorrow_only:
        extractsofamatchlinks(sport, tomorrow)
        extractsofamatches(sport, tomorrow)
        extractpmodds(sport, tomorrow)
        statsfromsofafiles(sport, tomorrow)

        getlivescores(sport,tomorrow)
        mergeallframes(sport, tomorrow)

        calculatestats(sport, tomorrow)
        findprematchdiscrepancies(tomorrow)
        findvaluebets(tomorrow)