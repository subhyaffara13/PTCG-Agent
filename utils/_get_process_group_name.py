
def _get_process_group_name(pg: ProcessGroup) -> str:
    return _world.pg_names.get(pg, "None")

