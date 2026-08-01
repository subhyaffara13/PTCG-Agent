
def match_to_number(match: re.Match[str], parse_float: ParseFloat) -> Any:
    if match.group("floatpart"):
        return parse_float(match.group())
    return int(match.group(), 0)


def match_to_number(match: re.Match[str], parse_float: ParseFloat) -> Any:
    if match.group("floatpart"):
        return parse_float(match.group())
    return int(match.group(), 0)


def match_to_number(match: re.Match, parse_float: ParseFloat) -> Any:
    if match.group("floatpart"):
        return parse_float(match.group())
    return int(match.group(), 0)


def match_to_number(match: re.Match[str], parse_float: ParseFloat) -> Any:
    if match.group("floatpart"):
        return parse_float(match.group())
    return int(match.group(), 0)


def match_to_number(match: "re.Match", parse_float: "ParseFloat") -> Any:
    if match.group("floatpart"):
        return parse_float(match.group())
    return int(match.group(), 0)

