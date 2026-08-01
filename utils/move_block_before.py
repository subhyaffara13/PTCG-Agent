
def move_block_before(block: list[fx.Node], target_node: fx.Node) -> None:
    for node in block:
        target_node.prepend(node)
        target_node = node

