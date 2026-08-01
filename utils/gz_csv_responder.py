
def gz_csv_responder(df):
    return gzip_bytes(csv_responder(df))

