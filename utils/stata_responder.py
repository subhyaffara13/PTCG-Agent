
def stata_responder(df):
    with BytesIO() as bio:
        df.to_stata(bio, write_index=False)
        return bio.getvalue()

