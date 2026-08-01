
def content_string(contents):
    res = ""
    for element in contents:
        if isinstance(element, tuple):
            continue
        res += element
    return res.strip()

