
def a_std(df):
    return df.resample("2D")["A"].std()

