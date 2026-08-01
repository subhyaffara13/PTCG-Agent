
def a_sum(df):
    return df.resample("2D")["A"].sum()

