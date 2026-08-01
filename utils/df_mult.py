
def df_mult(df_col, index):
    df_mult = df_col.copy()
    df_mult.index = pd.MultiIndex.from_arrays(
        [range(10), index], names=["index", "date"]
    )
    return df_mult

