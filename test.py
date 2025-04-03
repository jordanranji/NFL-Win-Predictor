from WR import rookieReceiving

rookieReceiving = rookieReceiving.loc[(rookieReceiving.position == "HB") & (rookieReceiving.routes > 136)]
rookieReceiving = rookieReceiving[["player", 'avg_depth_of_target', "Year"]]
print(rookieReceiving.sort_values(by = 'avg_depth_of_target', ascending=False))