
def html_responder(df):
    return df.to_html(index=False).encode("utf-8")

