
def get_compile_pg() -> dist.ProcessGroup | None:
    if (
        config.enable_compiler_collectives
        and dist.is_available()
        and dist.is_initialized()
    ):
        global _COMPILE_PG
        if _COMPILE_PG is None:
            # , timeout=datetime.timedelta(seconds=2)
            _COMPILE_PG = dist.distributed_c10d._new_group_with_tag(
                pg_tag="pt2_compile_pg"
            )
        return _COMPILE_PG

    return None

