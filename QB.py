import pandas as pd

#To combine all of the passing stats from QBs from 2017-2022

#start new part
qb = pd.read_csv("QBs/passing_09.csv")
qb = qb.loc[qb.position == "QB"]
qb["Year"] = 2009
qb = qb[['player', 'player_id', 'position', 'team_name', 'avg_depth_of_target',
       'completion_percent', 'franchise_id', 'grades_offense', 'grades_pass', 'grades_run', 
       'interceptions', 'passing_snaps', 'touchdowns', 'twp_rate', 'yards', 'ypa', 'Year']]

for i in range(10, 24):
    tempdf = pd.read_csv(f"QBs/passing_{i}.csv")

    tempdf = tempdf.loc[tempdf.position == "QB"]
    tempdf["Year"] = 2000 + i
    tempdf = tempdf[['player', 'player_id', 'position', 'team_name', 'avg_depth_of_target',
       'completion_percent', 'franchise_id', 'grades_offense', 'grades_pass', 'grades_run', 
       'interceptions', 'passing_snaps', 'touchdowns', 'twp_rate', 'yards', 'ypa', 'Year']]
    
    qb = pd.concat([qb, tempdf])
#End new part

qbsAll = qb.copy()
qbRookie = qb.copy()
qbsAll = qbsAll[["player_id", "Year", "grades_pass", "grades_run", "avg_depth_of_target"]]
qbsAll["Year"] = qbsAll["Year"] + 1

maxSnaps = qb.groupby(by = ['franchise_id', 'Year'])['passing_snaps'].max().reset_index()

qb = pd.merge(qb, maxSnaps, on=['franchise_id', 'Year', 'passing_snaps'])
qb = qb[["franchise_id", "Year", "player", "player_id"]]

qb = pd.merge(qb, qbsAll, how = "left", on = ["Year", "player_id"])

#This is for testing only now.

tester = tempdf.groupby(["team_name", "franchise_id"]).mean()