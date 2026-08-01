
def exclude_non_meta_vars(option: list[Constraint] | None) -> list[Constraint] | None:
    # If we had an empty list, keep it intact
    if not option:
        return option
    # However, if none of the options actually references meta vars, better remove
    # this constraint entirely.
    return [c for c in option if c.type_var.is_meta_var()] or None

