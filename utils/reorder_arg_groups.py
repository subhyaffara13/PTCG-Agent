
def reorder_arg_groups(groups: dict[ArgKind, list[RuntimeArg]]) -> list[RuntimeArg]:
    """Reorder argument groups to match their order in a format string."""
    return groups[ARG_POS] + groups[ARG_OPT] + groups[ARG_NAMED_OPT] + groups[ARG_NAMED]

