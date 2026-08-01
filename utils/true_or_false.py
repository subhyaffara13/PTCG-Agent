
def true_or_false(t: Type) -> ProperType:
    """
    Unrestricted version of t with both True-ish and False-ish values
    """
    t = get_proper_type(t)

    if isinstance(t, UnionType):
        new_items = [true_or_false(item) for item in t.items]
        return make_simplified_union(new_items, line=t.line, column=t.column)

    new_t = copy_type(t)
    new_t.can_be_true = new_t.can_be_true_default()
    new_t.can_be_false = new_t.can_be_false_default()
    return new_t

