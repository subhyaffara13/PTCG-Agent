
def get_extra_remote_code_state(cache_key: str) -> None:
    """
    Reads an additional PGO profile from the given cache key, and merges it with the default PGO profile.
    """
    global _CODE_STATE
    assert _CODE_STATE is not None

    remote_cache = get_remote_cache()
    if remote_cache is not None:
        with dynamo_timed(
            name := "pgo.get_extra_remote_code_state",
            log_pt2_compile_event=True,
            dynamo_compile_column_us="pgo_get_remote_code_state_time_us",
        ):
            CompileEventLogger.pt2_compile(name, cache_key=cache_key)
            code_state = lookup_remote_cache_entry(remote_cache, cache_key)
            log.info(
                "get_extra_code_state %s hit, %d entries",
                cache_key,
                len(code_state) if code_state is not None else 0,
            )
            if code_state is not None:
                assert not _CODE_STATE
                _CODE_STATE = code_state
                # log to tlparse
                trace_structured_artifact(
                    "get_extra_remote_code_state",
                    "string",
                    lambda: render_code_state(code_state),
                )

