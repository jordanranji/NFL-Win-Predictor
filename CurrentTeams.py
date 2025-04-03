import pandas as pd
import numpy as np
from TeamCreation import team_df, numericDF
from Standings import wins

block = pd.read_csv("Current/offense_blocking.csv")
qb = pd.read_csv("Current/passing_summary.csv")
rb = pd.read_csv("Current/rushing_summary.csv")
receiving = pd.read_csv("Current/receiving_summary.csv")
defense = pd.read_csv("Current/defense_summary.csv")

roster = pd.read_excel("Current/current_roster.xlsx")
roster["grades"] = np.nan

df_to_be_merged = []


qb = qb.loc[qb.position == "QB"]
qb = qb[['player', 'avg_depth_of_target', 'grades_pass', 'grades_run']]
qbdepth = qb[['player', 'avg_depth_of_target']].copy()
qbdepth["position"] = "qbdepth"
qbdepth = qbdepth.rename(columns={"avg_depth_of_target": "grades"})
qbpass = qb[['player', 'grades_pass']].copy()
qbpass["position"] = "qbpass"
qbpass = qbpass.rename(columns={"grades_pass": "grades"})
qbrun = qb[['player', 'grades_run']].copy()
qbrun["position"] = "qbrun"
qbrun = qbrun.rename(columns={"grades_run": "grades"})

df_to_be_merged.append(qbdepth)
df_to_be_merged.append(qbrun)
df_to_be_merged.append(qbpass)

#for rb only
rb = rb.loc[rb.position == "HB"]
rb = rb[['player', 'grades_run']]
rb["position"] = 'rb'
rb = rb.rename(columns={"grades_run": "grades"})
df_to_be_merged.append(rb)
#rb pass hither
rbcatch = receiving.loc[receiving.position == "HB"].copy()
rbcatch = rbcatch[['player', 'targeted_qb_rating']]
rbcatch['position'] = 'rbpass'
rbcatch = rbcatch.rename(columns={"targeted_qb_rating": "grades"})
df_to_be_merged.append(rbcatch)
#wrs (there has to be a better way of doing this)
wrone = receiving.loc[receiving.position == "WR"].copy()
wrtwo = receiving.loc[receiving.position == "WR"].copy()
wrthree = receiving.loc[receiving.position == "WR"].copy()
wrone = wrone[['player', 'grades_offense']]
wrone = wrone.rename(columns={"grades_offense": "grades"})
wrtwo = wrtwo[['player', 'grades_offense']]
wrtwo = wrtwo.rename(columns={"grades_offense": "grades"})
wrthree = wrthree[['player', 'grades_offense']]
wrthree = wrthree.rename(columns={"grades_offense": "grades"})
wrone['position'] = "wr1"
wrtwo['position'] = "wr2"
wrthree['position'] = "wr3"
df_to_be_merged.append(wrone)
df_to_be_merged.append(wrtwo)
df_to_be_merged.append(wrthree)

#blocking, how fun. Imma just do it without making hella new dataframes
block = block[["player", "grades_pass_block", "grades_run_block"]]
block_pos_list = ["ltpass", "ltrun", "lgpass", "lgrun", "cepass", "cerun", 
                  "rgpass", "rgrun", "rtpass", "rtrun", "tepass", "terun"]
blocking = block.copy()

for i in range(0, len(block_pos_list), 2):
    blocking["position"] = block_pos_list[i]
    blocking = blocking.rename(columns={"grades_pass_block": "grades"})
    roster = pd.merge(roster, blocking[["player", "position", "grades"]].copy(), how="left", on=["player", "position"], suffixes=('', '_del'))
    roster["grades"] = roster.grades.combine_first(roster.grades_del)
    roster = roster.drop(columns=["grades_del"])
    blocking["position"] = block_pos_list[i + 1]
    blocking = blocking.rename(columns={"grades": "grades_pass_block"})
    blocking = blocking.rename(columns={"grades_run_block": "grades"})
    roster = pd.merge(roster, blocking[["player", "position", "grades"]].copy(), how="left", on=["player", "position"], suffixes=('', '_del'))
    roster["grades"] = roster.grades.combine_first(roster.grades_del)
    roster = roster.drop(columns=["grades_del"])
    blocking = blocking.rename(columns={"grades": "grades_run_block"})
#blocking has been added!

#te for receiving here
te = receiving[["player", "targeted_qb_rating"]].copy()
te = te.rename(columns={"targeted_qb_rating": "grades"})
te["position"] = "te"
df_to_be_merged.append(te)

#Cb 1 and 2
cb1 = defense[defense.position == "CB"].copy()
cb1 = cb1[["player", "grades_coverage_defense"]]
cb1["position"] = "cb1"
cb2 = defense[defense.position == "CB"].copy()
cb2 = cb2[["player", "grades_coverage_defense"]]
cb2["position"] = "cb2"
cb1 = cb1.rename(columns={"grades_coverage_defense": "grades"})
cb2 = cb2.rename(columns={"grades_coverage_defense": "grades"})

roster = pd.merge(roster, cb1, how = "left", on = ["player", "position"], suffixes=("", "_del"))
roster["grades"] = roster["grades"].combine_first(roster["grades_del"])
roster = roster.drop(columns=["grades_del"])
roster = pd.merge(roster, cb2, how = "left", on = ["player", "position"], suffixes=("", "_del"))
roster["grades"] = roster["grades"].combine_first(roster["grades_del"])
roster = roster.drop(columns=["grades_del"])

#Rest of defense
defense = defense[["player", "grades_defense"]]
defense = defense.rename(columns={"grades_defense": "grades"})

defense_pos_list = ["lb1", "lb2", "s", "de1", "de2", "dt"]
for pos in defense_pos_list:
    defense["position"] = pos
    roster = pd.merge(roster, defense, how = "left", on=["player", "position"], suffixes=('', '_del'))
    roster["grades"] = roster["grades"].combine_first(roster["grades_del"])
    roster = roster.drop(columns=["grades_del"])

for df in df_to_be_merged:
    roster = pd.merge(roster, df[["player", "position", "grades"]], how="left", on=["player", "position"], suffixes=('', '_del'))
    roster["grades"] = roster.grades.combine_first(roster.grades_del)
    roster = roster.drop(columns=["grades_del"])

column = team_df.copy()
column = column.drop(columns=["franchise_id", "team_name", "Year"])
roster["column"] = list(column.columns) * 32

roster = pd.pivot_table(roster[["team", "franchise_id", "grades", "column"]], index = ["team", "franchise_id"], 
                        values = "grades", columns = ["column"])
roster = roster.fillna(numericDF.mean())


roster = pd.merge(roster.reset_index().rename(columns={"team": "team_name"}), wins.loc[wins.Year == 2024][["team_name", "W-L%"]], 
                  how = "left", on = ["team_name"], suffixes=('', '_prev'))
roster = roster.rename(columns={"W-L%": "W-L%_prev"})