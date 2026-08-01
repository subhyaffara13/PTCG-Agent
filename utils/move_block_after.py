
def move_block_after(block: list[fx.Node], target_node: fx.Node) -> None:
    for node in block:
        target_node.append(node)
        target_node = node

