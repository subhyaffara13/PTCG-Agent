
def lazy_tag_to_prefix() -> Dict[str, str]:
    """feature.name -> first prefix, used by the Swagger warmup JS plugin.
    Returns empty when the snapshot is loaded — the plugin is unnecessary
    because /openapi.json already has full route info."""
    from litellm.proxy._lazy_openapi_snapshot import load_snapshot

    if load_snapshot():
        return {}
    return {
        feat.name: feat.path_prefixes[0]
        for feat in LAZY_FEATURES
        if not feat.persistent_swagger_stub
    }

