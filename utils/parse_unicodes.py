
def parse_unicodes(s):
    import re

    s = re.sub(r"0[xX]", " ", s)
    s = re.sub(r"[<+>,;&#\\xXuU\n	]", " ", s)
    l = []
    for item in s.split():
        fields = item.split("-")
        if len(fields) == 1:
            l.append(int(item, 16))
        else:
            start, end = fields
            l.extend(range(int(start, 16), int(end, 16) + 1))
    return l

