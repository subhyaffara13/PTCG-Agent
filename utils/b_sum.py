
def b_sum(df):
    return df.resample("2D")["B"].sum()

