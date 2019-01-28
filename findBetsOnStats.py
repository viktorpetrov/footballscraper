from Stats import Stats
from localsettings import *
import pandas as pd
import numpy as np
from Telegram import *

games = pd.read_csv(path + 'allgames.csv')
games = games.loc[games['progress'] == 'live']

allstats = pd.DataFrame()

for index, row in games.iterrows():
    try:
        s = Stats(row['match_id']).df()
        allstats = allstats.append(s,sort=False)
    except:
        continue


#    ___           _           _
#   |_ _|_ __ ___ | |__   __ _| | __ _ _ __   ___ ___
#    | || '_ ` _ \| '_ \ / _` | |/ _` | '_ \ / __/ _ \
#    | || | | | | | |_) | (_| | | (_| | | | | (_|  __/
#   |___|_| |_| |_|_.__/ \__,_|_|\__,_|_| |_|\___\___|
#

imbalance = allstats[(allstats['dangerous attacks reldiff'] > 160) | (allstats['dangerous attacks reldiff'] < 45)]

for index, row in imbalance.iterrows():
    s = Stats(row['match_id'])
    f = s.flatjsonfile
    if (f['goals home'] <= f['goals away'] and f['dangerous attacks reldiff'] > 160) or (f['goals home'] >= f['goals away'] and f['dangerous attacks reldiff'] < 45):
        if f['timer'].isdigit() and int(f['timer']) > 65:
            print('Imbalance:\n' + str(s))
            Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "Imbalance", 'Imbalance: ' + str(s)))

#    ____
#   |  _ \ _ __ __ ___      __
#   | | | | '__/ _` \ \ /\ / /
#   | |_| | | | (_| |\ V  V /
#   |____/|_|  \__,_| \_/\_/
#

print('###############\n'
      '#### Draws ####\n'
      '###############\n')
draw = allstats[(allstats['goals home'] == allstats['goals away'])]
for index, row in draw.iterrows():
    s = Stats(row['match_id'])
    if s.flatjsonfile['timer'].isdigit() and int(s.flatjsonfile['timer']) > 79:
        print(s)
        Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "Late draw", 'Late Draw: ' + str(s)))

#    __  __                                    _
#   |  \/  | ___  _ __ ___    __ _  ___   __ _| |___
#   | |\/| |/ _ \| '__/ _ \  / _` |/ _ \ / _` | / __|
#   | |  | | (_) | | |  __/ | (_| | (_) | (_| | \__ \
#   |_|  |_|\___/|_|  \___|  \__, |\___/ \__,_|_|___/
#                            |___/

print('###############\n'
      '#### More Goals ####\n'
      '###############')

moregoals = allstats

moregoals['goals home'] = moregoals['goals home'].replace(np.nan).fillna(0)
moregoals['goals away'] = moregoals['goals away'].replace(np.nan).fillna(0)
moregoals['total goals'] = moregoals['goals home'].astype(int) + moregoals['goals away'].astype(int)
moregoals['shots on goal home'] = moregoals['shots on goal home'].replace(np.nan).fillna(0)
moregoals['shots on goal away'] = moregoals['shots on goal away'].replace(np.nan).fillna(0)
moregoals['shots off goal home'] = moregoals['shots off goal home'].replace(np.nan).fillna(0)
moregoals['shots off goal away'] = moregoals['shots off goal away'].replace(np.nan).fillna(0)

moregoals['total shots'] = moregoals['shots on goal home'].astype(int) + moregoals['shots on goal away'].astype(int) + \
                           moregoals['shots off goal home'].astype(int) + moregoals['shots off goal away'].astype(int)

lotsofshots = moregoals[(moregoals['total shots'] > 7) & (moregoals['total goals'] == 0)]
for index, row in lotsofshots.iterrows():
    s = Stats(row['match_id'])
    print(s)
    #Telegram().send_message(chat_id=-1001403993640, msg=(row['match_id'], "Goal imminent", 'Goal imminent: ' + str(s)))
