
def gz_json_responder(df):
    return gzip_bytes(json_responder(df))

