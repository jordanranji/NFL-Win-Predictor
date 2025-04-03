#Joining the pff grades at each position for each team each year
import pandas as pd
from QB import qb, qbsAll
from OL import lt, lg, ce, rg, rt, teBlocking, ol
from RB import maxRushes, rbTemp
from WR import wr, teMax, pcRB, wrMerged
from Defense import defense, d

team_df = lt[["franchise_id", "team_name", "Year"]]

#Converting to just the values we want, probably should have done this earlier but here we are
qb = qb[["franchise_id", "grades_pass", "grades_run", "avg_depth_of_target", "Year"]]
lt = lt[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
lg = lg[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
ce = ce[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
rg = rg[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
rt = rt[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
teBlocking = teBlocking[["franchise_id", "grades_pass_block", "grades_run_block", "Year"]]
rbRushing = maxRushes[["franchise_id", "grades_run", "Year"]]
teCatching = teMax[["franchise_id", "targeted_qb_rating", "Year"]]
rbReceiving = pcRB[["franchise_id", "targeted_qb_rating", "Year"]]

#We need to adjust the pff grades, fuckkkkkkkkk



toMerge = [
    (qb, "qb_"),
    (lt, "lt_"),
    (lg, "lg_"),
    (ce, "ce_"),
    (rg, "rg_"),
    (rt, "rt_"),
    (teBlocking, "teBlock_"),
    (teCatching, "te_"),
    (rbRushing, "rb_"),
    (rbReceiving, "rb_")
]

def addPosition(df, prefix, bigDaddy):
    df = df.set_index(["franchise_id", "Year"]).add_prefix(prefix)
    bigDaddy = pd.merge(bigDaddy, df, on = ["franchise_id", "Year"], how = "left")
    return bigDaddy

team_df = pd.merge(team_df, wr, how = "left", on = ["franchise_id", "Year"])


for df, prefix in toMerge:
    team_df = addPosition(df, prefix, team_df)

team_df = pd.merge(team_df, defense, how = "left", on = ["franchise_id", "Year"])
team_df = team_df.loc[team_df.Year != 2009]


numericDF = team_df.select_dtypes(include=float)
team_df = team_df.fillna(numericDF.mean())
#It's ready to add wins