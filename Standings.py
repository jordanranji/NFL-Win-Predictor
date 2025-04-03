import pandas as pd
from TeamCreation import team_df
from QB import tester

#Making the wins column!
wins = pd.read_csv("Wins/standings09.txt")
wins = wins[["Tm", "W-L%", "Pts", "PtsO"]]
wins["Year"] = 2009
wins["Tm"] = wins["Tm"].str.replace("St.", "Saint", regex=False) #Getting them in order for franchise_id to be appropriately added
#for_f_id = wins.sort_values(by = "Tm").reset_index()
#for_f_id["franchise_id"] = for_f_id.index + 1 #This actually might all be useless, I'm just gonna give them the 
                                                #up to date abbr. and merge with tester
#print(pd.merge(for_f_id, tester, how = "left", on = ["franchise_id"])) It worked!

for i in range(10, 24):
    tempDf = pd.read_csv(f"Wins/standings{i}.txt")
    tempDf = tempDf[["Tm", "W-L%", "Pts", "PtsO"]]
    tempDf["Year"] = 2000 + i
    wins = pd.concat([wins, tempDf])

wins.Tm = wins.Tm.str.replace('[+*]', '', regex=True)
name_converter = {
    "New England Patriots": "NE",
    "New York Jets": "NYJ",
    "Miami Dolphins": "MIA",
    "Buffalo Bills": "BUF",
    "Pittsburgh Steelers": "PIT",
    "Baltimore Ravens": "BLT",
    "Cleveland Browns": "CLV",
    "Cincinnati Bengals": "CIN",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Houston Texans": "HST",
    "Tennessee Titans": "TEN",
    "Kansas City Chiefs": "KC",
    "San Diego Chargers": "LAC",
    "Los Angeles Chargers": "LAC",
    "Oakland Raiders": "LV",
    "Las Vegas Raiders": "LV",
    "Denver Broncos": "DEN",
    "Philadelphia Eagles": "PHI",
    "New York Giants": "NYG",
    "Dallas Cowboys": "DAL",
    "Washington Redskins": "WAS",
    "Washington Football Team": "WAS",
    "Washington Commanders": "WAS",
    "Chicago Bears": "CHI",
    "Green Bay Packers": "GB",
    "Detroit Lions": "DET",
    "Minnesota Vikings": "MIN",
    "Atlanta Falcons": "ATL",
    "New Orleans Saints": "NO",
    "Tampa Bay Buccaneers": "TB",
    "Carolina Panthers": "CAR",
    "Seattle Seahawks": "SEA",
    "St. Louis Rams": "LA",
    "Saint Louis Rams": "LA",
    "Los Angeles Rams": "LA",
    "San Francisco 49ers": "SF",
    "Arizona Cardinals": "ARZ"
}
wins["Tm"] = wins["Tm"].replace(name_converter)
wins = wins.rename(columns={"Tm": "team_name"})
wins = pd.merge(wins, tester.reset_index()[["team_name", "franchise_id"]], how = "left", on = ["team_name"])
wins["franchise_id"] = wins["franchise_id"].astype(int)

team_df = pd.merge(team_df, wins, how = "left", on = ["Year", "franchise_id"])
team_df = team_df.drop(["team_name_y"], axis=1)
team_df = team_df.rename(columns={"team_name_x": "team_name"})

wins["Year"] = wins["Year"] + 1

team_df = pd.merge(team_df, wins[["franchise_id", "Year", "W-L%"]], how = "left", on = ["Year", "franchise_id"], suffixes=('', '_prev'))