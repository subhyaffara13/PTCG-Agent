
def a_mean(df):
    return df.resample("2D")["A"].mean()

