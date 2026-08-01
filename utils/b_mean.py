
def b_mean(df):
    return df.resample("2D")["B"].mean()

