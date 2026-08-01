
def sym_stride(a, dim):
    val = V.graph.current_node.meta["val"]
    if isinstance(val, torch.SymInt):
        return val.node.expr
    else:
        return int(val)


def sym_stride(func, *args, **kwargs):
    return None

