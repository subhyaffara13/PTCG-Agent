import os
from pathlib import Path


def get_outputs(graph: fx.Graph) -> list[fx.Node]:
    for node in graph.find_nodes(op="output"):
        return pytree.tree_leaves(node.args[0])
    raise AssertionError("No output node found")


def get_outputs(build_py):
    build_dir = Path(build_py.build_lib)
    return {
        os.path.relpath(x, build_dir).replace(os.sep, "/")
        for x in build_py.get_outputs()
    }

