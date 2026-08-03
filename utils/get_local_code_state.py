import os

def get_local_code_state(cache_key: str) -> defaultdict[CodeId, CodeState] | None:
    global _CODE_STATE
    path = code_state_path(cache_key)
    if path is not None and os.path.exists(path):
        with dynamo_timed(
            name := "pgo.get_local_code_state", log_pt2_compile_event=True
        ):
            CompileEventLogger.pt2_compile(name, cache_key=cache_key)
            # Read lock not necessary as we always write atomically write to
            # the actual location
            with open(path, "rb") as f:
                try:
                    content = f.read()
                    _CODE_STATE = pickle.loads(content)
                    CompileEventLogger.pt2_compile(name, cache_size_bytes=f.tell())
                except Exception:
                    log.warning(
                        "get_code_state failed while reading %s", path, exc_info=True
                    )
                else:
                    CacheArtifactManager.record_artifact(
                        PGOCacheArtifact.type(), cache_key, content
                    )
                    return hit(path, "local")
    return None

