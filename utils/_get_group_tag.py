
def _get_group_tag(pg: ProcessGroup) -> str:
    """Return the tag associated with ``pg``."""
    tag = _world.pg_to_tag[pg]
    tag = tag.removeprefix("user:")
    return tag

