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


class MeasureType:
    Base = 'Base'
    Advanced = 'Advanced'
    Misc = 'Misc'
    Scoring = 'Scoring'
    Usage = 'Usage'
    Defense = 'Defense'
    Default = Base

    measure_types = [Base, Advanced, Misc, Scoring, Usage, Defense]


class PerMode:
    Totals = 'Totals'
    PerGame = 'PerGame'
    Per100 = 'Per100Possessions'
    Per36 = 'Per36'
    Default = Totals


def build_params(season, season_type, measure_type, per_mode=PerMode.Totals):
    return (
        ('College', ''),
        ('Conference', ''),
        ('Country', ''),
        ('DateFrom', ''),
        ('DateTo', ''),
        ('Division', ''),
        ('DraftPick', ''),
        ('DraftYear', ''),
        ('GameScope', ''),
        ('GameSegment', ''),
        ('Height', ''),
        ('LastNGames', '0'),
        ('LeagueID', '00'),
        ('Location', ''),
        ('MeasureType', measure_type),
        ('Month', '0'),
        ('OpponentTeamID', '0'),
        ('Outcome', ''),
        ('PORound', '0'),
        ('PaceAdjust', 'N'),
        ('PerMode', per_mode),
        ('Period', '0'),
        ('PlayerExperience', ''),
        ('PlayerPosition', ''),
        ('PlusMinus', 'N'),
        ('Rank', 'N'),
        ('Season', season),
        ('SeasonSegment', ''),
        ('SeasonType', season_type),
        ('ShotClockRange', ''),
        ('StarterBench', ''),
        ('TeamID', '0'),
        ('TwoWay', '0'),
        ('VsConference', ''),
        ('VsDivision', ''),
        ('Weight', ''),
    )


def build_player_info_params(season, season_type, per_mode=PerMode.Totals):
    return (
        ('College', ''),
        ('Conference', ''),
        ('Country', ''),
        ('DateFrom', ''),
        ('DateTo', ''),
        ('Division', ''),
        ('DraftPick', ''),
        ('DraftYear', ''),
        ('GameScope', ''),
        ('GameSegment', ''),
        ('Height', ''),
        ('LastNGames', '0'),
        ('LeagueID', '00'),
        ('Location', ''),
        ('Month', '0'),
        ('OpponentTeamID', '0'),
        ('Outcome', ''),
        ('PORound', '0'),
        ('PerMode', per_mode),
        ('Period', '0'),
        ('PlayerExperience', ''),
        ('PlayerPosition', ''),
        ('Season', season),
        ('SeasonSegment', ''),
        ('SeasonType', season_type),
        ('ShotClockRange', ''),
        ('StarterBench', ''),
        ('TeamID', '0'),
        ('VsConference', ''),
        ('VsDivision', ''),
        ('Weight', ''),
    )


def call_and_save_player_data(season, season_type, measure_type):
    params = build_params(season=season, season_type=season_type, measure_type=measure_type)

    response = requests.get('https://stats.nba.com/stats/leaguedashplayerstats', headers=headers, params=params,
                            timeout=10)

    resp = response.json()['resultSets'][0]

    frame = pd.DataFrame(resp['rowSet'])
    frame.columns = resp['headers']

    frame.to_csv('./data/player_data_{}_{}_{}.csv'.format(measure_type, season, season_type))


def call_and_save_player_info(season, season_type):
    params = build_player_info_params(season=season, season_type=season_type)

    response = requests.get('https://stats.nba.com/stats/leaguedashplayerbiostats', headers=headers, params=params,
                            timeout=10)

    resp = response.json()['resultSets'][0]

    frame = pd.DataFrame(resp['rowSet'])
    frame.columns = resp['headers']

    frame.to_csv('./data/player_bios_{}_{}.csv'.format(season, season_type))


seasons = ['2010-11','2011-12','2012-13','2013-14','2014-15','2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

for season in seasons:
    call_and_save_player_info(season, 'Regular Season')
    for measure_type in MeasureType.measure_types:
        print(season, measure_type)
        call_and_save_player_data(season, 'Regular Season', measure_type)
        sleep(1.5)
