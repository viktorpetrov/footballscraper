import localsettings
import json
from pprint import pprint


class Stats:

    statsfolder = 'matches/pmodds/json/'

    def __init__(self, match_id):
        self.match_id = match_id
        filepath = localsettings.path + self.statsfolder + '{}.json'.format(self.match_id)
        print('initiating stats for match_id {}'.format(self.match_id))

        with open(filepath) as f:
            self.jsonfile = json.load(f)

        pprint(self.jsonfile)