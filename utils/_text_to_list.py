
def _text_to_list(txt):
    out = txt.strip("][\n").replace("'", "").split(', ')
    return None if out[0] == "" else out

