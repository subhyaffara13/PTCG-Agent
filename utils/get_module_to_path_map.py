
def get_module_to_path_map(graph: Graph) -> dict[str, str]:
    return {module: node.xpath for module, node in graph.items()}

