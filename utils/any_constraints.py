
def any_constraints(options: list[list[Constraint] | None], *, eager: bool) -> list[Constraint]:
    """Deduce what we can from a collection of constraint lists.

    It's a given that at least one of the lists must be satisfied. A
    None element in the list of options represents an unsatisfiable
    constraint and is ignored.  Ignore empty constraint lists if eager
    is true -- they are always trivially satisfiable.
    """
    if eager:
        valid_options = [option for option in options if option]
    else:
        valid_options = [option for option in options if option is not None]

    if not valid_options:
        return []

    if len(valid_options) == 1:
        return valid_options[0]

    if all(is_same_constraints(valid_options[0], c) for c in valid_options[1:]):
        # Multiple sets of constraints that are all the same. Just pick any one of them.
        return valid_options[0]

    if all(is_similar_constraints(valid_options[0], c) for c in valid_options[1:]):
        # All options have same structure. In this case we can merge-in trivial
        # options (i.e. those that only have Any) and try again.
        # TODO: More generally, if a given (variable, direction) pair appears in
        # every option, combine the bounds with meet/join always, not just for Any.
        trivial_options = select_trivial(valid_options)
        if trivial_options and len(trivial_options) < len(valid_options):
            merged_options = []
            for option in valid_options:
                if option in trivial_options:
                    continue
                merged_options.append([merge_with_any(c) for c in option])
            return any_constraints(list(merged_options), eager=eager)

    # If normal logic didn't work, try excluding trivially unsatisfiable constraint (due to
    # upper bounds) from each option, and comparing them again.
    filtered_options = [filter_satisfiable(o) for o in options]
    if filtered_options != options:
        return any_constraints(filtered_options, eager=eager)

    # Try harder: if that didn't work, try to strip typevars that aren't meta vars.
    # Note this is what we would always do, but unfortunately some callers may not
    # set the meta var status correctly (for historical reasons), so we use this as
    # a fallback only.
    filtered_options = [exclude_non_meta_vars(o) for o in options]
    if filtered_options != options:
        return any_constraints(filtered_options, eager=eager)

    # Otherwise, there are either no valid options or multiple, inconsistent valid
    # options. Give up and deduce nothing.
    return []

