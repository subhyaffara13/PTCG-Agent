
def csv_responder(df):
    return df.to_csv(index=False).encode("utf-8")

