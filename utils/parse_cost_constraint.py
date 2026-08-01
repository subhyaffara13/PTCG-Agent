
def parse_cost_constraint(source, constraints):
    "Parses a cost constraint."
    saved_pos = source.pos
    ch = source.get()
    if ch in ALPHA:
        # Syntax: constraint [("<=" | "<") cost]
        constraint = parse_constraint(source, constraints, ch)

        max_inc = parse_fuzzy_compare(source)

        if max_inc is None:
            # No maximum cost.
            constraints[constraint] = 0, None
        else:
            # There's a maximum cost.
            cost_pos = source.pos
            max_cost = parse_cost_limit(source)

            # Inclusive or exclusive limit?
            if not max_inc:
                max_cost -= 1

            if max_cost < 0:
                raise error("bad fuzzy cost limit", source.string, cost_pos)

            constraints[constraint] = 0, max_cost
    elif ch in DIGITS:
        # Syntax: cost ("<=" | "<") constraint ("<=" | "<") cost
        source.pos = saved_pos

        # Minimum cost.
        cost_pos = source.pos
        min_cost = parse_cost_limit(source)

        min_inc = parse_fuzzy_compare(source)
        if min_inc is None:
            raise ParseError()

        constraint = parse_constraint(source, constraints, source.get())

        max_inc = parse_fuzzy_compare(source)
        if max_inc is None:
            raise ParseError()

        # Maximum cost.
        cost_pos = source.pos
        max_cost = parse_cost_limit(source)

        # Inclusive or exclusive limits?
        if not min_inc:
            min_cost += 1
        if not max_inc:
            max_cost -= 1

        if not 0 <= min_cost <= max_cost:
            raise error("bad fuzzy cost limit", source.string, cost_pos)

        constraints[constraint] = min_cost, max_cost
    else:
        raise ParseError()

