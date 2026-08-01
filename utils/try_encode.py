
def try_encode(string, enc):
    "turn unicode encoding into a functional routine"
    try:
        return string.encode(enc)
    except UnicodeEncodeError:
        return None

