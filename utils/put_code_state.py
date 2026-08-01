
def put_code_state() -> None:
    if _CODE_STATE is None:
        log.info("put_code_state: never initialized, will not write")
        return

    if _CODE_STATE == _INIT_CODE_STATE:
        log.info("put_code_state: no change, skipping")
        return

    cache_key = get_cache_key()
    if cache_key is None:
        log.info("put_code_state: no cache key, skipping")
        return

    put_local_code_state(cache_key)
    put_remote_code_state(cache_key)
    if (sticky_write := torch.compiler.config.pgo_extra_write_key) is not None:
        extra_write_key = get_extra_cache_key(sticky_write)
        if extra_write_key is not None:
            put_remote_code_state(extra_write_key)

