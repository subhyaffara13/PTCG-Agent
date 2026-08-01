
def _replace_observer_or_dequant_stub_with_dequantize_node(
    node: Node, graph: Graph
) -> None:
    call_custom_module_node = node.args[0]
    if not isinstance(call_custom_module_node, Node):
        raise AssertionError(
            f"Expecting the for call custom module node to be a Node, but got {call_custom_module_node}"
        )
    node.replace_all_uses_with(call_custom_module_node)
    graph.erase_node(node)
    _insert_dequantize_node(call_custom_module_node, graph)

