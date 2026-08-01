
def tips_df(datapath):
    """DataFrame with the tips dataset."""
    return read_csv(datapath("io", "data", "csv", "tips.csv"))

