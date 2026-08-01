
def put_local_code_state(cache_key: str) -> None:
    with dynamo_timed(name := "pgo.put_local_code_state", log_pt2_compile_event=True):
        CompileEventLogger.pt2_compile(name, cache_key=cache_key)
        assert _CODE_STATE is not None

        pickled_code = pickle.dumps(_CODE_STATE)

        CacheArtifactManager.record_artifact(
            PGOCacheArtifact.type(), cache_key, pickled_code
        )

        meta = write_local_impl(cache_key, pickled_code)
        if meta is None:
            log.info("put_code_state: local cache disabled")
            return
        path, size = meta

        CompileEventLogger.pt2_compile(name, cache_size_bytes=size)
        log.info("put_code_state: wrote local %s, %d entries", path, len(_CODE_STATE))
        trace_structured_artifact(
            "put_local_code_state",
            "string",
            lambda: render_code_state(_CODE_STATE),
        )

