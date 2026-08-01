
def _parse_pattern(source, info):
    "Parses a pattern, eg. 'a|b|c'."
    branches = [parse_sequence(source, info)]
    while source.match("|"):
        branches.append(parse_sequence(source, info))

    if len(branches) == 1:
        return branches[0]
    return Branch(branches)

