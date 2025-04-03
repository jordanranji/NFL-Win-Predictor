import pandas as pd
#Combining rb stats 



rbTemp = pd.read_csv("RBs/rushing_09.csv")
rbTemp = rbTemp[['player', 'player_id', 'position', 'team_name',
       'attempts', 'franchise_id', 'grades_offense', 'grades_run']]
rbTemp = rbTemp.loc[rbTemp.position == "HB"]
rbTemp["Year"] = 2009

for i in range(10, 24):
    tempDf = pd.read_csv(f"RBs/rushing_{i}.csv")
    tempDf = tempDf[['player', 'player_id', 'position', 'team_name',
       'attempts', 'franchise_id', 'grades_offense', 'grades_run']]
    tempDf = tempDf.loc[tempDf.position == "HB"]
    tempDf["Year"] = 2000 + i
    rbTemp = pd.concat([rbTemp, tempDf])


rbsAll = rbTemp.copy()
rbsAll["Year"] = rbsAll["Year"] + 1

maxRushes = rbTemp.sort_values(by = ["franchise_id", "Year", "attempts", "grades_run"], ascending=[True, True, False, False])

rbsAll = rbsAll[["player_id", "grades_run", "Year"]]

maxRushes = maxRushes[["franchise_id", "Year", "player", "player_id"]]
maxRushes = maxRushes.groupby(["franchise_id", "Year"]).head(1).reset_index()

maxRushes = pd.merge(maxRushes, rbsAll, how = "left", on = ["player_id", "Year"])