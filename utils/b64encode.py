
def b64encode(b):
    s = base64.b64encode(b)
    # Line-break at 76 chars.
    items = []
    while s:
        items.append(tostr(s[:76]))
        items.append("\n")
        s = s[76:]
    return strjoin(items)

