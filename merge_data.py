import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

seasons = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

"""

bpm

"""

for season in seasons:
    print(season)
    bio = pd.read_csv('data/player_bios_{}_Regular Season.csv'.format(season))[
        ['PLAYER_ID', 'PLAYER_NAME', "TEAM_ID", 'TEAM_ABBREVIATION', 'AGE', 'PLAYER_HEIGHT', 'PLAYER_WEIGHT', 'GP', 'AST_PCT']]
    base = pd.read_csv('data/player_data_Base_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'W', 'L', 'MIN']]
    advanced = pd.read_csv('data/player_data_Advanced_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'POSS']]

    defense = pd.read_csv('data/player_data_Defense_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PCT_BLK']]
    scoring = pd.read_csv('data/player_data_Scoring_{}_Regular Season.csv'.format(season))[['PLAYER_ID','PCT_FGA_3PT']]

    cut = pd.read_csv('data/synergy_Cut_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'POSS_PCT', 'PPP', 'PERCENTILE']]
    transition = pd.read_csv('data/synergy_Transition_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

    iso = pd.read_csv('data/synergy_Isolation_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
    ball_handler = pd.read_csv('data/synergy_PRBallHandler_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

    rollman = pd.read_csv('data/synergy_PRRollman_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
    postup = pd.read_csv('data/synergy_Postup_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

    spotup = pd.read_csv('data/synergy_Spotup_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
    handoff = pd.read_csv('data/synergy_Handoff_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

    offscreen = pd.read_csv('data/synergy_OffScreen_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
    putbacks = pd.read_csv('data/synergy_OffRebound_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]

    misc = pd.read_csv('data/synergy_Misc_{}_Regular Season.csv'.format(season))[['PLAYER_ID', 'PERCENTILE', 'PPP', 'POSS_PCT']]
    misc.columns = ['PLAYER_ID', 'PERCENTILE_misc', 'PPP_misc', 'POSS_PCT_misc']

    merged = bio\
        .merge(base, on='PLAYER_ID')\
        .merge(advanced, on='PLAYER_ID')\
        .merge(defense, on='PLAYER_ID')\
        .merge(scoring, on='PLAYER_ID')

    syn1 = cut.merge(transition, on='PLAYER_ID', suffixes=('_cut','_transition'))
    syn2 = iso.merge(ball_handler, on='PLAYER_ID', suffixes=('_iso', '_ball_handler'))
    syn3 = rollman.merge(postup, on='PLAYER_ID', suffixes=('_rollman', '_postup'))
    syn4 = spotup.merge(handoff, on='PLAYER_ID', suffixes=('_spotup', '_handoff'))
    syn5 = offscreen.merge(putbacks, on='PLAYER_ID', suffixes=('_offscreen', '_putbacks'))

    syn = syn1.merge(syn2, on='PLAYER_ID').merge(syn3, on='PLAYER_ID').merge(syn4, on='PLAYER_ID').merge(syn5, on='PLAYER_ID').merge(misc, on='PLAYER_ID')

    all = merged.merge(syn, on='PLAYER_ID')

    all['SEASON'] = season


    all.to_csv('results/all_data_{}.csv'.format(season))

