
def parse_set_union(source, info):
    "Parses a set union ([x||y])."
    items = [parse_set_symm_diff(source, info)]
    while source.match("||"):
        items.append(parse_set_symm_diff(source, info))

    if len(items) == 1:
        return items[0]
    return SetUnion(info, items)

