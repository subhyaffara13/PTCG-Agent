import time

def process_fresh_modules(graph: Graph, modules: list[str], manager: BuildManager) -> None:
    """Process the modules in one group of modules from their cached data.

    This can be used to process an SCC of modules. This involves loading the tree (i.e.
    module symbol tables) from cache file and then fixing cross-references in the symbols.
    """
    t0 = time.time()
    for id in modules:
        graph[id].load_tree()
    t1 = time.time()
    for id in modules:
        graph[id].fix_cross_refs()
    t2 = time.time()
    manager.add_stats(process_fresh_time=t2 - t0, load_tree_time=t1 - t0)

