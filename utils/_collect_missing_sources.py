
def _collect_missing_sources(all_sources: OrderedSet[str]) -> OrderedSet[str]:
    from torch._dynamo.variables.builder import is_dynamic_source

    global _KNOWN_DYNAMIC_SOURCES
    missing_sources: OrderedSet[str] = OrderedSet()
    for src in all_sources:
        if src in _KNOWN_DYNAMIC_SOURCES:
            continue
        elif is_dynamic_source(src):
            _KNOWN_DYNAMIC_SOURCES.add(src)
            continue
        missing_sources.add(src)
    return missing_sources

