
def parse_fuzzy_item(source, constraints):
    "Parses a fuzzy setting item."
    saved_pos = source.pos
    try:
        parse_cost_constraint(source, constraints)
    except ParseError:
        source.pos = saved_pos

        parse_cost_equation(source, constraints)

