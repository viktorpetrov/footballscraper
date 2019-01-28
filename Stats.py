import localsettings
import json
import pandas as pd
import collections


class Stats:

    statsfolder = 'matches/pmodds/json/'

    @staticmethod
    def flatten(d, parent_key='', sep=' '):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k.lower() if parent_key else k.lower()
            if isinstance(v, collections.MutableMapping):
                items.extend(Stats.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def __init__(self, match_id):
        self.match_id = match_id
        filepath = localsettings.path + self.statsfolder + '{}.json'.format(self.match_id)
        #print('initiating stats for match_id {}'.format(self.match_id))

        with open(filepath) as f:
            self.jsonfile = json.load(f)
            self.flatjsonfile = Stats.flatten(self.jsonfile)

    def df(self):
        return pd.DataFrame.from_records([self.flatjsonfile])

    def __str__(self):
        s = self.flatjsonfile

        ret_str = '#### Match: {}-{} ({}) ####\n' \
                  'score {}\': {} - {}'.format(s.get('team home'),s.get('team away'),s.get('match_id'),s.get('timer'),s.get('goals home'),s.get('goals away'))

        ret_str += '\nPossession {}-{}\n' \
                   '\nAttacks {}-{}\n' \
                  'Dangerous attacks {}-{}\n' \
                  'Shots on goal {}-{}\n' \
                  'Shots off goal {}-{}\n' \
                  'Corner kicks {}-{}\n'.format(s.get('ball possession home'), s.get('ball possession away'), s.get('attacks home'),
                                                s.get('attacks away'),
                                                s.get('dangerous attacks home'),
                                                s.get('dangerous attacks away'),
                                                s.get('shots on goal home'),
                                                s.get('shots on goal away'),
                                                s.get('shots off goal home'),
                                                s.get('shots off goal away'),
                                                s.get('corner kicks home'),
                                                s.get('corner kicks away'))

        ret_str += 'Red cards {}-{}\n'.format(s.get('red cards home'),
                                     s.get('red cards away'))

        return ret_str
