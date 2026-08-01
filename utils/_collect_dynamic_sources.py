
def _collect_dynamic_sources(code_state: CodeState) -> OrderedSet[str]:
    dynamic_sources: OrderedSet[str] = OrderedSet()
    for src, fs in code_state.automatic_dynamic.items():
        dynamic = False
        if isinstance(fs.size, tuple):
            dynamic = auto_dynamic in fs.size  # type: ignore[operator]
        elif fs.scalar == auto_dynamic:
            dynamic = True
        if dynamic:
            dynamic_sources.add(src)
    return dynamic_sources

