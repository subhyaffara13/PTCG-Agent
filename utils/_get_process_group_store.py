
def _get_process_group_store(pg: ProcessGroup) -> Store:
    return _world.pg_map[pg][1]

