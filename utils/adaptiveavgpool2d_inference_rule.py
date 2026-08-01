
def adaptiveavgpool2d_inference_rule(n: Node, module_instance):
    """
    The input and output sizes should be the same except for the last
    two dimensions taken from the input, which represent width and height
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))
    if isinstance(n.args[0].type, TensorType):
        output_type = adaptiveavgpool2d_check(n.args[0].type, module_instance)
        n.type = get_greatest_upper_bound(n.type, output_type)
    return n.type

