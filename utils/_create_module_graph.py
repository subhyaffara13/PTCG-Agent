
def _create_module_graph(nodes: set[str]) -> dict[str, set[str]]:
  graph = {}

  for source in nodes:
    deps = set()
    for val in sys.modules[source].__dict__.values():
      if inspect.ismodule(val) and val.__name__ in nodes:
        deps.add(val.__name__)
    graph[source] = deps

  return graph

