import os

def _dependencies_graph(filename: str, dep_info: dict[str, set[str]]) -> str:
    """Write dependencies as a dot (graphviz) file."""
    done = {}
    printer = DotBackend(os.path.splitext(os.path.basename(filename))[0], rankdir="LR")
    printer.emit('URL="." node[shape="box"]')
    for modname, dependencies in sorted(dep_info.items()):
        sorted_dependencies = sorted(dependencies)
        done[modname] = 1
        printer.emit_node(modname)
        for depmodname in sorted_dependencies:
            if depmodname not in done:
                done[depmodname] = 1
                printer.emit_node(depmodname)
    for depmodname, dependencies in sorted(dep_info.items()):
        for modname in sorted(dependencies):
            printer.emit_edge(modname, depmodname)
    return printer.generate(filename)

