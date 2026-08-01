
def options_snapshot(module: str, manager: BuildManager) -> dict[str, object]:
    """Make compact snapshot of options for a module.

    Separately store only the options we may compare individually, and take a hash
    of everything else. If --debug-cache is specified, fall back to full snapshot.
    """
    cloned = manager.options.clone_for_module(module)
    if manager.options.debug_cache:
        # Build full options snapshot for debugging purposes.
        platform_opt, values = cloned.select_options_affecting_cache()
        result: dict[str, object] = {"platform": platform_opt}
        for key, val in zip(OPTIONS_AFFECTING_CACHE_NO_PLATFORM, values):
            result[key] = val
        return result
    cache = manager.options_snapshot_cache
    cached = cache.get(cloned)
    if cached is None:
        platform_opt, values = cloned.select_options_affecting_cache()
        buf = WriteBuffer()
        write_json_value(buf, cast(JsonValue, values))
        cached = (platform_opt, hash_digest(buf.getvalue()))
        cache[cloned] = cached
    return {"platform": cached[0], "other_options": cached[1]}

