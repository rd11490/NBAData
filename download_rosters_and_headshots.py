import requests
import shutil
import pandas as pd
import time

class NBATeams:
    AtlantaHawks = '1610612737'
    BostonCeltics = '1610612738'
    BrooklynNets = '1610612751'
    CharlotteHornets = '1610612766'
    ChicagoBulls = '1610612741'
    ClevelandCavaliers = '1610612739'
    DallasMavericks = '1610612742'
    DenverNuggets = '1610612743'
    DetroitPistons = '1610612765'
    GoldenStateWarriors = '1610612744'
    HoustonRockets = '1610612745'
    IndianaPacers = '1610612754'
    LosAngelesClippers = '1610612746'
    LosAngelesLakers = '1610612747'
    MemphisGrizzlies = '1610612763'
    MiamiHeat = '1610612748'
    MilwaukeeBucks = '1610612749'
    MinnesotaTimberwolves = '1610612750'
    NewOrleansPelicans = '1610612740'
    NewYorkKnicks = '1610612752'
    OklahomaCityThunder = '1610612760'
    OrlandoMagic = '1610612753'
    Philadelphia76ers = '1610612755'
    PhoenixSuns = '1610612756'
    PortlandTrailBlazers = '1610612757'
    SacramentoKings = '1610612758'
    SanAntonioSpurs = '1610612759'
    TorontoRaptors = '1610612761'
    UtahJazz = '1610612762'
    WashingtonWizards = '1610612764'

    Teams = [
        AtlantaHawks,
        BostonCeltics,
        BrooklynNets,
        CharlotteHornets,
        ChicagoBulls,
        ClevelandCavaliers,
        DallasMavericks,
        DenverNuggets,
        DetroitPistons,
        GoldenStateWarriors,
        HoustonRockets,
        IndianaPacers,
        LosAngelesClippers,
        LosAngelesLakers,
        MemphisGrizzlies,
        MiamiHeat,
        MilwaukeeBucks,
        MinnesotaTimberwolves,
        NewOrleansPelicans,
        NewYorkKnicks,
        OklahomaCityThunder,
        OrlandoMagic,
        Philadelphia76ers,
        PhoenixSuns,
        PortlandTrailBlazers,
        SacramentoKings,
        SanAntonioSpurs,
        TorontoRaptors,
        UtahJazz,
        WashingtonWizards
    ]

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw==',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

seasons = ['2010-11','2011-12','2012-13','2013-14','2014-15','2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
players_list = []

for season in seasons:
    for team in NBATeams.Teams:
        print(team)

        params = (
            ('season', '2019-20'),
            ('leagueId', '00'),
            ('teamId', team),
        )

        response = requests.get('http://stats.nba.com/stats/commonteamroster', headers=headers, params=params, timeout=5)
        jsn = response.json()
        resp = jsn['resultSets'][0]
        players = resp['rowSet']

        p_frame = pd.DataFrame(players)
        p_frame.columns = resp['headers']
        players_list.append(p_frame)

        # def img_url(player, team, season):
        #     return 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/{}/{}/260x190/{}.png'.format(team, season, player)
        # for p in players:
        #     team_id = p[0]
        #     season = p[1]
        #     player_id = p[-1]
        #     player_name = p[3]
        #     url = img_url(player_id, team_id, season)
        #     response = requests.get(url, stream=True)
        #     with open('pictures/{}_{}_{}_{}.png'.format(player_name, player_id, team_id, season), 'wb') as out_file:
        #         shutil.copyfileobj(response.raw, out_file)
        #     del response
        time.sleep(2)

frame = pd.concat(players_list)
print(frame)
frame.to_csv('results/rosters.csv')