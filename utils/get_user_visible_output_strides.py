
def get_user_visible_output_strides(g: Graph) -> dict[Node, tuple[int, ...]]:
    ret: dict[Node, tuple[int, ...]] = {}
    output_node = g.find_nodes(op="output")[0]

    if "user_visible_output_idxs" not in output_node.meta:
        return ret

    if not isinstance(output_node.args[0], torch.fx.Node):
        output_node_args = output_node.args[0]
    else:
        output_node_args = output_node.args

    for idx, node in enumerate(output_node_args):
        if idx in output_node.meta["user_visible_output_idxs"]:
            ret[node] = output_node.meta["original_output_strides"][idx]
    return ret

