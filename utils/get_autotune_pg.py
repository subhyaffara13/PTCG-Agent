
def get_autotune_pg() -> dist.ProcessGroup | None:
    if dist.is_available() and dist.is_initialized():
        global _AUTOTUNE_PG
        if _AUTOTUNE_PG is None:
            _AUTOTUNE_PG = dist.distributed_c10d._new_group_with_tag(
                pg_tag="pt2_distributed_autotune_pg"
            )
        return _AUTOTUNE_PG

    return None

