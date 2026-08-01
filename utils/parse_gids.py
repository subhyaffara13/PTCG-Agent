
def parse_gids(s):
    l = []
    for item in s.replace(",", " ").split():
        fields = item.split("-")
        if len(fields) == 1:
            l.append(int(fields[0]))
        else:
            l.extend(range(int(fields[0]), int(fields[1]) + 1))
    return l

