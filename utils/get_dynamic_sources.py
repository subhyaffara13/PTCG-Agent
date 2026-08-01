
def get_dynamic_sources() -> set[str]:
    global _DYNAMIC_SOURCES, _DYNAMIC_SOURCES_CONFIG_HASH

    current_hash = hash(torch.compiler.config.dynamic_sources)

    # If we have already calculated the sources and the config hasn't changed, return cached result
    if _DYNAMIC_SOURCES is not None and _DYNAMIC_SOURCES_CONFIG_HASH == current_hash:
        return _DYNAMIC_SOURCES

    # Config has changed or first time, (re)calculate the sources
    _DYNAMIC_SOURCES = {
        s
        for s in torch.compiler.config.dynamic_sources.replace(" ", "").split(",")
        if s
    }
    _DYNAMIC_SOURCES_CONFIG_HASH = current_hash

    return _DYNAMIC_SOURCES

