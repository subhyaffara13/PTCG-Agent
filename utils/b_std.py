
def b_std(df):
    return df.resample("2D")["B"].std()

