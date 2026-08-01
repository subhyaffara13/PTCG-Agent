
def parsed_114(datapath):
    dta14_114 = datapath("io", "data", "stata", "stata5_114.dta")
    parsed_114 = read_stata(dta14_114, convert_dates=True)
    parsed_114.index.name = "index"
    return parsed_114

