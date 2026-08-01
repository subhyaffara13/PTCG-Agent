
def _is_valid_hybrid_shard_pg_type(process_group: Any) -> bool:
    return (
        isinstance(process_group, tuple)
        and len(process_group) == 2
        and all(isinstance(pg, dist.ProcessGroup) for pg in process_group)
    )

