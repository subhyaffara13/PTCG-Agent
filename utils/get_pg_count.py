
def get_pg_count() -> int:
    """
    Return the number of process groups.

    """
    return _world.group_count

