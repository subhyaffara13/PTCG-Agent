
def parquetpyarrow_reponder(df):
    return df.to_parquet(index=False, engine="pyarrow")

