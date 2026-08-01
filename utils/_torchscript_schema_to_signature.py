
def _torchscript_schema_to_signature(
    ts_schema: torch._C.FunctionSchema,
) -> inspect.Signature:
    # Cached as it's called in the hot path of FakeTensor dispatch
    cache_key = ts_schema.name, ts_schema.overload_name
    cache_val = _SCHEMA_TO_SIGNATURE_CACHE.get(cache_key)
    if cache_val is not None:
        return cache_val

    res = _torchscript_schema_to_signature_impl(ts_schema)
    _SCHEMA_TO_SIGNATURE_CACHE[cache_key] = res
    return res

