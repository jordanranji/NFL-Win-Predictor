import pandas as pd
import numpy as np
from BANG import pred
from CurrentTeams import roster
from Standings import team_df

roster = roster[["team_name", "franchise_id"]]
win_proj = pd.read_excel(r"Wins/Win Totals.xlsx")

win_proj = pd.merge(win_proj, roster, how = "left", on = ["team_name"])
win_proj = win_proj.sort_values(by = ["franchise_id"])

win_proj["Projected Wins"] = pred * 17

win_proj["Absolute Difference"] = np.abs(win_proj["Projected Wins"] - win_proj["Wins"])
win_proj["Difference"] = win_proj["Projected Wins"] - win_proj["Wins"]

win_proj = win_proj.sort_values(by=["Absolute Difference"], ascending=False)


win_proj.to_excel('win_proj.xlsx')