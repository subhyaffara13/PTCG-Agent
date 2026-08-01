
def df_grouper_resample(df):
    return df.groupby(pd.Grouper(freq="2D"))

