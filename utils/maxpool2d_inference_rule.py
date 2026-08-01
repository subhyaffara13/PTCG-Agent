
def maxpool2d_inference_rule(n: Node, module_instance):
    """
    Given a MaxPool2D instance and a node check the following conditions:
    - Input size matches size 3 or 4
    - Current node type is consistent with the output type we will calculate
    - Input size matches output size and the last two dimensions of the output
      are w_out and h_out. The remaining dimensions are the same as the input
    - Our final result is the greatest upper bound of the output we calculate
      and the current node type.
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))
    if isinstance(n.args[0].type, TensorType):
        output = maxpool2d_check(n.args[0].type, module_instance)
        n.type = get_greatest_upper_bound(output, n.type)
    return n.type

