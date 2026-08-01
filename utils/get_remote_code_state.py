
def get_remote_code_state(cache_key: str) -> defaultdict[CodeId, CodeState] | None:
    global _CODE_STATE
    remote_cache = get_remote_cache()
    if remote_cache is not None:
        with dynamo_timed(
            name := "pgo.get_remote_code_state",
            log_pt2_compile_event=True,
            dynamo_compile_column_us="pgo_get_remote_code_state_time_us",
        ):
            CompileEventLogger.pt2_compile(name, cache_key=cache_key)
            code_state = lookup_remote_cache_entry(remote_cache, cache_key, name)
            if code_state is not None:
                _CODE_STATE = code_state
                return hit(cache_key, "remote")
    return None

