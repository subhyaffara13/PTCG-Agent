
def _parse_re_match(node_match: re.Match) -> dict | str:
    # If the regex has named groups, return a dict of those groups
    if node_match.groupdict():
        return {key: val for key, val in node_match.groupdict().items() if val is not None}
    # Otherwise the regex must have exactly one unnamed group, and we return that
    else:
        groups = list(node_match.groups())
        if len(groups) > 1:
            raise ValueError(f"Regex has multiple unnamed groups!\nGroups: {groups}\n")
        elif len(groups) == 0:
            raise ValueError(f"Regex has no capture groups:\n\n{node_match.group(0)}")
        return groups[0]

