import pandas as pd
#Pulling together receiving stats for tight ends, rbs, and wrs 

wrMerged = pd.read_csv("WRs/receiving_09.csv")
wrMerged = wrMerged[['player', 'player_id', 'avg_depth_of_target', 'position', 'team_name', 'inline_snaps', 'slot_snaps', 'wide_snaps',
       'franchise_id', 'grades_offense', 'targeted_qb_rating', 'routes']]
wrMerged["Year"] = 2009

for i in range(10, 24):
    tempDf = pd.read_csv(f"WRs/receiving_{i}.csv")
    tempDf = tempDf[['player', 'player_id', 'avg_depth_of_target', 'position', 'team_name', 'inline_snaps', 'slot_snaps', 'wide_snaps',
       'franchise_id', 'grades_offense', 'targeted_qb_rating', 'routes']]
    tempDf["Year"] = 2000 + i
    wrMerged = pd.concat([wrMerged, tempDf])


rookieReceiving = wrMerged.copy()

wrCatch = wrMerged.loc[wrMerged.position == "WR"]
teCatch = wrMerged.loc[wrMerged.position == "TE"]
rbCatch = wrMerged.loc[wrMerged.position == "HB"]


#Finding the top 3 receivers for each team
wrSort = wrCatch.sort_values(by = ["franchise_id", "Year", "routes", "grades_offense"], ascending=[True, True, False, False])
top = wrSort.groupby(["franchise_id", "Year"]).head(3).reset_index(drop = True)
#print(top[top.duplicated(subset=["franchise_id", "Year", "routes"], keep = False)])
#In this case, DHop and AJ Green ran the same number of routes, but we're gonna obviously place DHop as WR1

wrMerged = wrMerged[["player_id", "Year", "grades_offense", "targeted_qb_rating"]]
wrMerged["Year"] = wrMerged["Year"] + 1

#Finding TE1 for each team
teCatch = teCatch.sort_values(by = ['franchise_id', 'Year', 'routes'], ascending=[True, True, False])
teMax = teCatch.groupby(['franchise_id', 'Year']).head(1).reset_index(drop = True)

#Finding receiving rb for each team
pcRB = rbCatch.sort_values(by = ["franchise_id", "Year", "routes", "targeted_qb_rating"], ascending=[True, True, False, False])
pcRB = pcRB.groupby(["franchise_id", "Year"]).head(1).reset_index()

top = top[["player", "player_id", "team_name", "franchise_id", "Year"]]
top = pd.merge(top, wrMerged, how = "left", on = ["Year", "player_id"])

pcRB = pcRB[["player", "player_id", "team_name", "franchise_id", "Year"]]
pcRB = pd.merge(pcRB, wrMerged, how = "left", on = ["Year", "player_id"])
pcRB = pcRB[["player", "player_id", "Year", "franchise_id", "team_name", "targeted_qb_rating"]]

teMax = teMax[["player", "player_id", "Year", "franchise_id", "team_name"]]
teMax = pd.merge(teMax, wrMerged, how = "left", on = ["Year", "player_id"])
teMax = teMax[["player", "player_id", "Year", "franchise_id", "team_name", "targeted_qb_rating"]]
#Here's where we will have to add values for all of the players that are NaN


#Need to pivot wrs to make them all in one row.
wr = top[["franchise_id", "Year", "grades_offense"]].copy()
prefixList = ["wr1_", "wr2_", "wr3_"]
wr['prefix'] = prefixList * 480   #This feels so rudimentary

wr = wr.pivot_table(values = "grades_offense", index = ["franchise_id", "Year"], columns="prefix")
wr.columns = [f'{column}grades_offense' for column in wr.columns]