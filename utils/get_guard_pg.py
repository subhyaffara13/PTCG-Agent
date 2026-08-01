
def get_guard_pg() -> dist.ProcessGroup | None:
    if dist.is_available() and dist.is_initialized():
        global _GUARD_PG
        if _GUARD_PG is None:
            _GUARD_PG = dist.distributed_c10d._new_group_with_tag(pg_tag="pt2_guard_pg")
        return _GUARD_PG

    return None

