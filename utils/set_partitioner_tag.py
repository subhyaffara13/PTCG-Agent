
def set_partitioner_tag(tag: str) -> Generator[None, None, None]:
    meta_key = "partitioner_tag"
    if not fx_traceback.has_preserved_node_meta():
        raise AssertionError("expected preserved node meta")

    original_val = fx_traceback.current_meta.get(meta_key, None)
    fx_traceback.current_meta[meta_key] = tag
    try:
        yield
    finally:
        fx_traceback.current_meta[meta_key] = original_val

