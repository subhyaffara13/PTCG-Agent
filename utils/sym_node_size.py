
def sym_node_size(node: fx.Node) -> int:
    if isinstance(node.meta["val"], (torch.SymInt, torch.SymBool)):
        return 1
    if not isinstance(node.meta["val"], torch.SymFloat):
        raise AssertionError(
            f"expected node.meta['val'] to be SymFloat, got {type(node.meta['val'])}"
        )
    return 4

