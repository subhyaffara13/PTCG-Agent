
def _get_dtype_from_loopbodies(loop_bodies):
    dtypes = OrderedSet[torch.dtype]()
    for loop_body in loop_bodies:
        graphs = [loop_body.root_block.graph] + [
            body.graph for body in list(loop_body.subblocks.values())
        ]
        for graph in graphs:
            for node in graph.nodes:
                if node.op != "call_method":
                    continue
                dtypes.add(node.meta[OptimizationContext.key].dtype)
    return dtypes

