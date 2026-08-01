
def put_remote_code_state(cache_key: str, extra_code_state: bool = False) -> None:
    event_name = (
        "put_remote_code_state"
        if not extra_code_state
        else "put_extra_remote_code_state"
    )
    with dynamo_timed(
        name := f"pgo.{event_name}",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="pgo_put_remote_code_state_time_us",
    ):
        CompileEventLogger.pt2_compile(name, cache_key=cache_key)
        assert _CODE_STATE is not None

        remote_cache = get_remote_cache()

        if remote_cache is None:
            log.info("%s: remote cache disabled", event_name)
            return

        content = pickle.dumps(_CODE_STATE)
        CompileEventLogger.pt2_compile(name, cache_size_bytes=len(content))
        cache_data: JsonDataTy = {
            "data": base64.b64encode(content).decode("ascii"),
        }
        remote_cache.put(cache_key, cache_data)
        log.info(
            "%s: wrote remote %s, %d entries", event_name, cache_key, len(_CODE_STATE)
        )
        # TODO: don't log this multiple times
        trace_structured_artifact(
            event_name,
            "string",
            lambda: render_code_state(_CODE_STATE),
        )

