
def propagate_scatter_value(out_node: Node) -> bool:
    # The backward of scatter.value always has value=0 (gradient of a constant),
    # so S * scatter(x, idx, 0) = scatter(S*x, idx, 0) holds.
    value = out_node.args[3]
    if value != 0:
        return False
    return propagate_general_copy(out_node)

