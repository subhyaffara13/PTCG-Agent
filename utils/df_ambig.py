
def df_ambig(df):
    """DataFrame with levels 'L1' and 'L2' and labels 'L1' and 'L3'"""
    df = df.set_index(["L1", "L2"])

    df["L1"] = df["L3"]

    return df

