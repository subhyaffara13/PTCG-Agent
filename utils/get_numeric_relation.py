
def get_numeric_relation(value, other_value, sort_key_fn):
    """Compares two values and returns their relation or None."""
    value = sort_key_fn(value)
    other_value = sort_key_fn(other_value)
    if value == other_value:
        return Relation.EQ
    if value < other_value:
        return Relation.LT
    if value > other_value:
        return Relation.GT
    return None

