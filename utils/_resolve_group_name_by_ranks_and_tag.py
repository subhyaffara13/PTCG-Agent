
def _resolve_group_name_by_ranks_and_tag(ranks: list[int], tag: str) -> GroupName:
    # TODO(yifu): remove this function once ranks + tag is not a supported
    # identifier for process group for functional collectives.
    group = _find_pg_by_ranks_and_tag(tag, ranks)
    if group is None:
        raise ValueError("")
    return group.group_name

