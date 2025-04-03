from RB import rbTemp
from QB import qbRookie
from Defense import dRookie
from WR import rookieReceiving
from OL import olRookie
import pandas as pd



draft19 = pd.read_csv(r"Rookie Prediction/nflDraft/class2019.csv")
draft19["Year"] = 2019
draft20 = pd.read_csv(r"Rookie Prediction/nflDraft/class2020.csv")
draft20["Year"] = 2020
draft21 = pd.read_csv(r"Rookie Prediction/nflDraft/class2021.csv")
draft21["Year"] = 2021
draft22 = pd.read_csv(r"Rookie Prediction/nflDraft/class2022.csv")
draft22["Year"] = 2022
draft23 = pd.read_csv(r"Rookie Prediction/nflDraft/class2023.csv")
draft23["Year"] = 2023
draft = pd.concat([draft19, draft20, draft21, draft22, draft23])


draft["Pos"] = draft["Pos"].replace("DE", "ED")
draft["Pos"] = draft["Pos"].replace("DT", "DI")
draft["Pos"] = draft["Pos"].replace("RB", "HB")

rookieReceiving["snaps"] = rookieReceiving["slot_snaps"] + rookieReceiving["wide_snaps"] + rookieReceiving["inline_snaps"]

rbTemp = rbTemp[["player", "player_id", "position", "attempts", "Year", "grades_offense"]]
qbRookie = qbRookie[["player", "player_id", "position", "passing_snaps", "Year", "grades_offense"]]
dRookie = dRookie[["player", "player_id", "position", "snap_counts_defense", "Year", "grades_defense"]]
rookieReceiving = rookieReceiving[["player", "player_id", "position", "snaps", "Year", "grades_offense"]]
olRookie = olRookie[["player", "player_id", "position", "snap_counts_offense", "Year", "grades_offense"]]
print()
listofdf = [rbTemp, qbRookie, dRookie, rookieReceiving, olRookie]

def renaming(df):
    dict1 = {"player": "Player", "player_id": "player_id", "position": "Pos", df.columns[3]: "snaps", "Year": "Year", df.columns[5]: "grade"}
    df.rename(columns=dict1, inplace=True)
    return df

list1 = []
for i in range(5):
    list1.append(renaming(listofdf[i].copy()))

rb = list1[0]
rb = rb.loc[(rb.Pos == "HB") | (rb.Pos == "FB")]
qb = list1[1]
qb = qb.loc[qb.Pos == "QB"]
d = list1[2]
d.loc[(d.Pos == "S") | (d.Pos == "ED") | (d.Pos == "DI") | (d.Pos == "CB") | (d.Pos == "LB")]
wr = list1[3]
wr.loc[(wr.Pos == "WR") | (wr.Pos == "TE")]
ol = list1[4]
ol = ol.loc[(ol.Pos == "T") | (ol.Pos == "G") | (ol.Pos == "C")]


players = pd.concat([rb, qb, d, wr, ol])

draft = draft[["Rnd", "Pick", "Player", "Pos", "Age", "Year"]] 

#Is it better to make a model by position or to add position as a parameter? If linear gonna have to do the first

draft = pd.merge(draft, players, how = "left", on = ["Player", "Pos", "Year"])
draft = draft.loc[draft.snaps.notna()]
draft = draft.sort_values(by = ["snaps"], ascending=[False])
draft = draft.groupby(by = ["Player", "Pos", "Year"]).head(1).reset_index()