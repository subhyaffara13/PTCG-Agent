
def _split_autocast(gm: torch.fx.GraphModule) -> torch.fx.GraphModule:
    """
    split_autocast creates a new graph module that splits the input graph module into multiple submodules
    based on the `_enter_autocast` and `_exit_autocast` nodes. It doesn't mutate the input graph module.

    Nodes between the **outer-most** `_enter_autocast` and `_exit_autocast(_enter_autocast)` are split
    into a submodule. Nested autocast regions are not split.
    `_enter_autocast` and `_exit_autocast(_enter_autocast)` nodes are in the submodule as well.

    Below is an example of splitting. A, B, C, D, E are blocks of non-autocast nodes in the original graph
    module. Nodes marked with the same number are grouped into the same submodule.
    A               # 0
    enter_autocast  # 1
    B               # 1
    exit_autocast   # 1
    C               # 2
    enter_autocast  # 3
    D               # 3
    exit_autocast   # 3
    E               # 4
    """
    enter_autocast_node_stack: list[torch.fx.Node] = []
    first_node_after_outer_most_exit: bool = False

    def node_call_back(node: torch.fx.Node) -> bool:
        nonlocal enter_autocast_node_stack, first_node_after_outer_most_exit
        increment_id = False
        if first_node_after_outer_most_exit or (
            len(enter_autocast_node_stack) == 0 and _is_enter_autocast_node(node)
        ):
            if len(enter_autocast_node_stack) != 0:
                raise AssertionError(
                    f"expected empty stack, got {len(enter_autocast_node_stack)} items"
                )
            first_node_after_outer_most_exit = False
            increment_id = True
        if _is_enter_autocast_node(node):
            enter_autocast_node_stack.append(node)
        elif _is_exit_autocast_node(node):
            if len(enter_autocast_node_stack) == 0:
                raise AssertionError("enter_autocast_node_stack must not be empty")
            last_enter_autocast_node = enter_autocast_node_stack.pop()
            if node.args[0] != last_enter_autocast_node:
                raise AssertionError("exit node args[0] must match last enter node")
            if len(enter_autocast_node_stack) == 0:
                # next node should be in the next submodule since
                # autocast block ends
                first_node_after_outer_most_exit = True
        return increment_id

    return sequential_split(gm, node_call_back)

