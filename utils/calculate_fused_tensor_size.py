
def calculate_fused_tensor_size(split_node: torch.fx.Node, indices: list[int]) -> int:
    """
    Calculate the fused tensor size in the indices
    """
    fused_tensor_size = 0
    for i in range(len(split_node.args[1])):  # type: ignore[arg-type]
        if i in indices:
            fused_tensor_size += split_node.args[1][i]  # type: ignore[operator, assignment, index]
    # pyrefly: ignore [bad-return]
    return fused_tensor_size

