
def parse_cost_limit(source):
    "Parses a cost limit."
    cost_pos = source.pos
    digits = parse_count(source)

    try:
        return int(digits)
    except ValueError:
        pass

    raise error("bad fuzzy cost limit", source.string, cost_pos)

