import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

seasons = ['2010-11','2011-12','2012-13','2013-14','2014-15','2015-16', '2016-17', '2017-18', '2018-19', '2019-20']


for season in seasons:
    print(season)
    bio = pd.read_csv('data/player_bios_{}_Regular Season.csv'.format(season))

    teams = bio[['TEAM_ID', 'TEAM_ABBREVIATION']].drop_duplicates()

    bio = bio[
        ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'AGE', 'PLAYER_HEIGHT', 'PLAYER_WEIGHT', 'GP', 'AST_PCT']]

    base = pd.read_csv('data/player_data_Base_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'TEAM_ID', 'W', 'L', 'MIN']]
    advanced = pd.read_csv('data/player_data_Advanced_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'TEAM_ID', 'POSS']]

    defense = pd.read_csv('data/player_data_Defense_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'TEAM_ID', 'PCT_BLK']]
    scoring = pd.read_csv('data/player_data_Scoring_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'TEAM_ID', 'PCT_FGA_3PT']]

    merged = base\
        .merge(advanced, on=['PLAYER_ID', 'TEAM_ID'])\
        .merge(defense, on=['PLAYER_ID', 'TEAM_ID'])\
        .merge(scoring, on=['PLAYER_ID', 'TEAM_ID'])\
        .merge(bio, on=['PLAYER_ID', 'TEAM_ID'], how='outer')

    if season not in ['2010-11','2011-12']:
        cut = pd.read_csv('data/synergy_Cut_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'POSS_PCT', 'PPP', 'PERCENTILE']]
        transition = pd.read_csv('data/synergy_Transition_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

        iso = pd.read_csv('data/synergy_Isolation_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
        ball_handler = pd.read_csv('data/synergy_PRBallHandler_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

        rollman = pd.read_csv('data/synergy_PRRollman_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
        postup = pd.read_csv('data/synergy_Postup_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

        spotup = pd.read_csv('data/synergy_Spotup_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
        handoff = pd.read_csv('data/synergy_Handoff_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

        offscreen = pd.read_csv('data/synergy_OffScreen_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
        putbacks = pd.read_csv('data/synergy_OffRebound_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

        misc = pd.read_csv('data/synergy_Misc_{}_Regular Season.csv'.format(season))[
            ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
        misc.columns = ['PLAYER_ID', 'TEAM_ID', 'PERCENTILE_misc', 'PPP_misc', 'POSS_PCT_misc']

        syn1 = cut.merge(transition, on=['PLAYER_ID', 'TEAM_ID'], suffixes=('_cut','_transition'), how='outer')
        syn2 = iso.merge(ball_handler, on=['PLAYER_ID', 'TEAM_ID'], suffixes=('_iso', '_ball_handler'), how='outer')
        syn3 = rollman.merge(postup, on=['PLAYER_ID', 'TEAM_ID'], suffixes=('_rollman', '_postup'), how='outer')
        syn4 = spotup.merge(handoff, on=['PLAYER_ID', 'TEAM_ID'], suffixes=('_spotup', '_handoff'), how='outer')
        syn5 = offscreen.merge(putbacks, on=['PLAYER_ID', 'TEAM_ID'], suffixes=('_offscreen', '_putbacks'), how='outer')

        syn = syn1.merge(syn2, on=['PLAYER_ID', 'TEAM_ID'], how='outer')\
            .merge(syn3, on=['PLAYER_ID', 'TEAM_ID'], how='outer')\
            .merge(syn4, on=['PLAYER_ID', 'TEAM_ID'], how='outer')\
            .merge(syn5, on=['PLAYER_ID', 'TEAM_ID'], how='outer')\
            .merge(misc, on=['PLAYER_ID', 'TEAM_ID'], how='outer')

        merged = merged.drop(columns=['TEAM_ID'])

        all = merged.merge(syn, on=['PLAYER_ID'], how='outer')
    else:
        all = merged

    all['SEASON'] = season

    all = all.merge(teams, on='TEAM_ID')


    all.to_csv('results/all_data_{}.csv'.format(season))

