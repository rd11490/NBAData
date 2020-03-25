import requests
import pandas as pd
from time import sleep


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw==',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/players/transition/',
    'Accept-Language': 'en-US,en;q=0.9',
}


class PlayTypes:
    Transition = 'Transition'
    Isolation = 'Isolation'
    PRBallHandler = 'PRBallHandler'
    PRRollman = 'PRRollman'
    Postup = 'Postup'
    Spotup = 'Spotup'
    Handoff = 'Handoff'
    Cut = 'Cut'
    OffScreen = 'OffScreen'
    Misc = 'Misc'
    Putbacks = 'OffRebound'

    play_types = [Transition, Isolation, PRBallHandler, PRRollman, Postup, Spotup, Handoff, Cut, OffScreen, Misc, Putbacks]


class OffenseDefense:
    Offense = 'offensive'

    Default = Offense


class PerMode:
    Totals = 'Totals'
    PerGame = 'PerGame'
    Per100 = 'Per100Possessions'
    Per36 = 'Per36'
    Default = Totals


def build_params(season, season_type, play_type, per_mode=PerMode.Default, offense_defense=OffenseDefense.Default):
    return (
        ('LeagueID', '00'),
        ('PerMode', per_mode),
        ('PlayType', play_type),
        ('PlayerOrTeam', 'P'),
        ('SeasonType', season_type),
        ('SeasonYear', season),
        ('TypeGrouping', offense_defense),
    )


def call_and_save_play_type_data(season, season_type, play_type):
    params = build_params(season=season, season_type=season_type, play_type=play_type)
    response = requests.get('https://stats.nba.com/stats/synergyplaytypes', headers=headers, params=params, timeout=10)

    resp = response.json()['resultSets'][0]

    frame = pd.DataFrame(resp['rowSet'])
    frame.columns = resp['headers']

    frame.to_csv('./data/synergy_{}_{}_{}.csv'.format(play_type,season,season_type))


seasons = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

for season in seasons:
    for play_type in PlayTypes.play_types:
        print(season, play_type)
        call_and_save_play_type_data(season, 'Regular Season', play_type)
        sleep(1.5)
