import pandas as pd


d = pd.read_csv("Defense/defense_09.csv")
d = d[["player", "player_id", "position", "franchise_id", 
       "grades_coverage_defense", "grades_defense", "grades_pass_rush_defense", "grades_run_defense",
       'snap_counts_defense']]
d["Year"] = 2009

for i in range(10, 24):
    tempDf = pd.read_csv(f"Defense/defense_{i}.csv")
    tempDf = tempDf[["player", "player_id", "position", "franchise_id", 
       "grades_coverage_defense", "grades_defense", "grades_pass_rush_defense", "grades_run_defense",
       'snap_counts_defense']]
    tempDf["Year"] = 2000 + i
    d = pd.concat([d, tempDf])

dRookie = d.copy()
d = d.sort_values(by = ["franchise_id", "Year", "snap_counts_defense"], ascending=[True, True, False])

cb = d.loc[d.position == "CB"].groupby(['franchise_id', 'Year']).head(2).reset_index()
lb = d.loc[d.position == "LB"].groupby(["franchise_id", "Year"]).head(2).reset_index()
s = d.loc[d.position == "S"].groupby(["franchise_id", "Year"]).head(1).reset_index()
de = d.loc[d.position == "ED"].groupby(["franchise_id", "Year"]).head(2).reset_index()
dt = d.loc[d.position == "DI"].groupby(["franchise_id", "Year"]).head(1).reset_index()

d = d[["player_id", "Year", "grades_coverage_defense", "grades_defense"]]
d["Year"] = d["Year"] + 1

#CB
cb = cb[["player", "player_id", "Year", "franchise_id"]]
cb = pd.merge(cb, d, how = "left", on = ["player_id", "Year"])
cb = cb[["franchise_id", "Year", "grades_coverage_defense"]]
cb["rank"] = "cb" + cb.groupby(["franchise_id", "Year"])["Year"].rank(method = "first", ascending=False).astype(int).astype(str) + "_grades_coverage_defense"
cb = cb.pivot_table(values = "grades_coverage_defense", index = ["franchise_id", "Year"], columns="rank", dropna = False)

#LB
lb = lb[["player", "player_id", "Year", "franchise_id"]]
lb = pd.merge(lb, d, how = "left", on = ["player_id", "Year"])
lb = lb[["franchise_id", "Year", "grades_defense"]]
lb["rank"] = "lb" + lb.groupby(["franchise_id", "Year"])["Year"].rank(method = "first", ascending=False).astype(int).astype(str) + "_grades_defense"
lb = lb.pivot_table(values = "grades_defense", index = ["franchise_id", "Year"], columns="rank", dropna = False)
#S
s = s[["player", "player_id", "Year", "franchise_id"]]
s = pd.merge(s, d, how = "left", on = ["player_id", "Year"])
s = s[["franchise_id", "Year", "grades_defense"]]
s = s.rename(columns={"grades_defense": "s_grades_defense"})
#DE
de = de[["player", "player_id", "Year", "franchise_id"]]
de = pd.merge(de, d, how = "left", on = ["player_id", "Year"])
de = de[["franchise_id", "Year", "grades_defense"]]
de["rank"] = "de" + de.groupby(["franchise_id", "Year"])["Year"].rank(method = "first", ascending=False).astype(int).astype(str) + "_grades_defense"
de = de.pivot_table(values = "grades_defense", index = ["franchise_id", "Year"], columns="rank", dropna = False)
#DT
dt = dt[["player", "player_id", "Year", "franchise_id"]]
dt = pd.merge(dt, d, how = "left", on = ["player_id", "Year"])
dt = dt[["franchise_id", "Year", "grades_defense"]]
dt = dt.rename(columns={"grades_defense": "dt_grades_defense"})

defense = pd.merge(cb, lb, how = "left", on = ["franchise_id", "Year"])
defense = pd.merge(defense, s, how = "left", on = ["franchise_id", "Year"])
defense = pd.merge(defense, de, how = "left", on = ["franchise_id", "Year"])
defense = pd.merge(defense, dt, how = "left", on = ["franchise_id", "Year"])