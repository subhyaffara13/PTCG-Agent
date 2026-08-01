
def get_unbacked_sources() -> set[str]:
    global _UNBACKED_SOURCES, _UNBACKED_SOURCES_CONFIG_HASH

    current_hash = hash(torch.compiler.config.unbacked_sources)

    # If we have already calculated the sources and the config hasn't changed, return cached result
    if _UNBACKED_SOURCES is not None and _UNBACKED_SOURCES_CONFIG_HASH == current_hash:
        return _UNBACKED_SOURCES

    # Config has changed or first time, (re)calculate the sources
    _UNBACKED_SOURCES = {
        s
        for s in torch.compiler.config.unbacked_sources.replace(" ", "").split(",")
        if s
    }
    _UNBACKED_SOURCES_CONFIG_HASH = current_hash

    return _UNBACKED_SOURCES

