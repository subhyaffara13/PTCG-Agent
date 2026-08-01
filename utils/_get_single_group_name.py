
def _get_single_group_name(regex: re.Pattern) -> Hashable:
    if regex.groupindex:
        return next(iter(regex.groupindex))
    else:
        return None

