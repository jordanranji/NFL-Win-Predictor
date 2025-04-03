import pandas as pd

ol = pd.read_csv("Blocking/blocking_09.csv")
ol = ol[['player', 'player_id', 'position', 'team_name', 'franchise_id', "grades_offense",
       'grades_pass_block', 'grades_run_block', 'snap_counts_offense', 'snap_counts_ce', 'snap_counts_lg', 
       'snap_counts_lt', 'snap_counts_rg', 'snap_counts_rt', 'snap_counts_te']]
ol["Year"] = 2009

for i in range(10, 24):
    tempDf = pd.read_csv(f"Blocking/blocking_{i}.csv")
    tempDf = tempDf[['player', 'player_id', 'position', 'team_name', 'franchise_id', "grades_offense",
       'grades_pass_block', 'grades_run_block', 'snap_counts_offense', 'snap_counts_ce', 'snap_counts_lg', 
       'snap_counts_lt', 'snap_counts_rg', 'snap_counts_rt', 'snap_counts_te']]
    tempDf["Year"] = 2000 + i
    ol = pd.concat([ol, tempDf])

olRookie = ol.copy()

teBlocking = ol.loc[ol.position == "TE"]
teBlocking = teBlocking.sort_values(by=["franchise_id", "Year", "snap_counts_te", "grades_run_block"], ascending=[True, True, False, False])
teBlocking = teBlocking.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

rt = ol.sort_values(by = ["franchise_id", "Year", "snap_counts_rt", "grades_run_block"], ascending = [True, True, False, False])
rt = rt.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

rg = ol.sort_values(by = ["franchise_id", "Year", "snap_counts_rg", "grades_run_block"], ascending = [True, True, False, False])
rg = rg.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

ce = ol.sort_values(by = ["franchise_id", "Year", "snap_counts_ce", "grades_run_block"], ascending = [True, True, False, False])
ce = ce.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

lg = ol.sort_values(by = ["franchise_id", "Year", "snap_counts_lg", "grades_run_block"], ascending = [True, True, False, False])
lg = lg.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

lt = ol.sort_values(by = ["franchise_id", "Year", "snap_counts_lt", "grades_run_block"], ascending = [True, True, False, False])
lt = lt.groupby(by = ["franchise_id", "Year"]).head(1).reset_index()

ol = ol[["player_id", "Year", "grades_pass_block", "grades_run_block"]]
ol["Year"] = ol["Year"] + 1


rt = rt[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
rt = pd.merge(rt, ol, how = "left", on = ["player_id", "Year"])
lt = lt[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
lt = pd.merge(lt, ol, how = "left", on = ["player_id", "Year"])
lg = lg[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
lg = pd.merge(lg, ol, how = "left", on = ["player_id", "Year"])
rg = rg[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
rg = pd.merge(rg, ol, how = "left", on = ["player_id", "Year"])
ce = ce[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
ce = pd.merge(ce, ol, how = "left", on = ["player_id", "Year"])
teBlocking = teBlocking[["player", "player_id", "position", "team_name", "Year", "franchise_id"]]
teBlocking = pd.merge(teBlocking, ol, how = "left", on = ["player_id", "Year"])