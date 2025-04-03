import pandas as pd
from draftToRookie import draft


rblock18 = pd.read_csv(r"Rookie Prediction\rookieBlocking\block2018.csv")
rblock18["Year"] = 2019
rblock19 = pd.read_csv(r"Rookie Prediction\rookieBlocking\block2019.csv")
rblock19["Year"] = 2020
rblock20 = pd.read_csv(r"Rookie Prediction\rookieBlocking\block2020.csv")
rblock20["Year"] = 2021
rblock21 = pd.read_csv(r"Rookie Prediction\rookieBlocking\block2021.csv")
rblock21["Year"] = 2022
rblock22 = pd.read_csv(r"Rookie Prediction\rookieBlocking\block2022.csv")
rblock22["Year"] = 2023
block = pd.concat([rblock18, rblock19, rblock20, rblock21, rblock22])

rdefense18 = pd.read_csv(r"Rookie Prediction\rookieDefense\def2018.csv")
rdefense18["Year"] = 2019
rdefense19 = pd.read_csv(r"Rookie Prediction\rookieDefense\def2019.csv")
rdefense19["Year"] = 2020
rdefense20 = pd.read_csv(r"Rookie Prediction\rookieDefense\def2020.csv")
rdefense20["Year"] = 2021
rdefense21 = pd.read_csv(r"Rookie Prediction\rookieDefense\def2021.csv")
rdefense21["Year"] = 2022
rdefense22 = pd.read_csv(r"Rookie Prediction\rookieDefense\def2022.csv")
rdefense22["Year"] = 2023
defense = pd.concat([rdefense18, rdefense19, rdefense20, rdefense21, rdefense22])

rpassing18 = pd.read_csv(r"Rookie Prediction\rookiePassing\pass2018.csv")
rpassing18["Year"] = 2019
rpassing19 = pd.read_csv(r"Rookie Prediction\rookiePassing\pass2019.csv")
rpassing19["Year"] = 2020
rpassing20 = pd.read_csv(r"Rookie Prediction\rookiePassing\pass2020.csv")
rpassing20["Year"] = 2021
rpassing21 = pd.read_csv(r"Rookie Prediction\rookiePassing\pass2021.csv")
rpassing21["Year"] = 2022
rpassing22 = pd.read_csv(r"Rookie Prediction\rookiePassing\pass2022.csv")
rpassing22["Year"] = 2023
passing = pd.concat([rpassing18, rpassing19, rpassing20, rpassing21, rpassing22])

rreceiving18 = pd.read_csv(r"Rookie Prediction\rookieReceiving\rec2018.csv")
rreceiving18["Year"] = 2019
rreceiving19 = pd.read_csv(r"Rookie Prediction\rookieReceiving\rec2019.csv")
rreceiving19["Year"] = 2020
rreceiving20 = pd.read_csv(r"Rookie Prediction\rookieReceiving\rec2020.csv")
rreceiving20["Year"] = 2021
rreceiving21 = pd.read_csv(r"Rookie Prediction\rookieReceiving\rec2021.csv")
rreceiving21["Year"] = 2022
rreceiving22 = pd.read_csv(r"Rookie Prediction\rookieReceiving\rec2022.csv")
rreceiving22["Year"] = 2023
receiving = pd.concat([rreceiving18, rreceiving19, rreceiving20, rreceiving21, rreceiving22])

rrushing18 = pd.read_csv(r"Rookie Prediction\rookieRushing\rush2018.csv")
rrushing18["Year"] = 2019 #Might have to change the year to match
rrushing19 = pd.read_csv(r"Rookie Prediction\rookieRushing\rush2019.csv")
rrushing19["Year"] = 2020
rrushing20 = pd.read_csv(r"Rookie Prediction\rookieRushing\rush2020.csv")
rrushing20["Year"] = 2021
rrushing21 = pd.read_csv(r"Rookie Prediction\rookieRushing\rush2021.csv")
rrushing21["Year"] = 2022
rrushing22 = pd.read_csv(r"Rookie Prediction\rookieRushing\rush2022.csv")
rrushing22["Year"] = 2023
rushing = pd.concat([rrushing18, rrushing19, rrushing20, rrushing21, rrushing22])

rushing = rushing[["player", "player_id", "position", "Year", "grades_offense"]]
receiving = receiving[["player", "player_id", "position", "Year", "grades_offense"]]
passing = passing[["player", "player_id", "position", "Year", "grades_offense"]]
block = block[["player", "player_id", "position", "Year", "grades_offense"]]
defense = defense[["player", "player_id", "position", "Year", "grades_defense"]]


listofdf = [rushing, receiving, passing, block, defense]

def renaming(df):
    dict1 = {"player": "Player", "player_id": "player_id", "position": "Pos", "Year": "Year", df.columns[4]: "college_grade"}
    df.rename(columns=dict1, inplace=True)
    return df

list1 = []
for i in range(5):
    list1.append(renaming(listofdf[i].copy()))

college_rb = list1[0]
college_rb = college_rb.loc[(college_rb.Pos == "HB") | (college_rb.Pos == "FB")]
college_wr = list1[1]
college_wr = college_wr.loc[(college_wr.Pos == "WR") | (college_wr.Pos == "TE")]
college_qb = list1[2]
college_qb = college_qb.loc[college_qb.Pos == "QB"]
college_ol = list1[3]
college_ol = college_ol.loc[(college_ol.Pos == "T") | (college_ol.Pos == "G") | (college_ol.Pos == "C")]
college_d = list1[4]
college_d = college_d.loc[(college_d.Pos == "S") | (college_d.Pos == "ED") | (college_d.Pos == "DI") | (college_d.Pos == "CB") | (college_d.Pos == "LB")]

college_players = pd.concat([college_rb, college_qb, college_d, college_wr, college_ol])

college_players = pd.merge(draft, college_players, how = "left", on = ["Player", "player_id", "Pos", "Year"])
college_players = college_players.loc[college_players["college_grade"].notna()]


#predicting "grade" off of college_grade, pick, age, and position
college_rb = college_players.loc[(college_players.Pos == "HB") | (college_players.Pos == "FB")]

college_wr = college_players.loc[(college_players.Pos == "WR") | (college_players.Pos == "TE")]

college_qb = college_players.loc[college_players.Pos == "QB"]

college_ol = college_players.loc[(college_players.Pos == "T") | (college_players.Pos == "G") | (college_players.Pos == "C")]

college_d = college_players.loc[(college_players.Pos == "S") | (college_players.Pos == "ED") | (college_players.Pos == "DI") | (college_players.Pos == "CB") | (college_players.Pos == "LB")]

