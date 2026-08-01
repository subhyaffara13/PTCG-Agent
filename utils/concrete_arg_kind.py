
def concrete_arg_kind(kind: ArgKind) -> ArgKind:
    """Find the concrete version of an arg kind that is being passed."""
    if kind == ARG_OPT:
        return ARG_POS
    elif kind == ARG_NAMED_OPT:
        return ARG_NAMED
    else:
        return kind

