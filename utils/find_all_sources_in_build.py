
def find_all_sources_in_build(
    graph: mypy.build.Graph, extra: Sequence[BuildSource] = ()
) -> list[BuildSource]:
    result = list(extra)
    seen = {source.module for source in result}
    for module, state in graph.items():
        if module not in seen:
            result.append(BuildSource(state.path, module))
    return result

