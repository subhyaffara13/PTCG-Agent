
def bn2d_inference_rule(n: Node, module_instance):
    """
    Given a BatchNorm2D instance and a node check the following conditions:
    - the input type can be expanded to a size 4 tensor: t =  (x_1, x_2, x_3, x_4)
    - the current node type can be expanded to a size 4 tensor: t' =  (x_1', x_2', x_3', x_4')
    - t is consistent with t'
    - x_2 is consistent with the module's num_features
    - x_2' is consistent with the module's num_features
    output type: the more precise type of t and t'
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    n.args[0].type = expand_to_tensor_dim(n.args[0].type, 4)
    arg_type = n.args[0].type
    n.type = expand_to_tensor_dim(n.type, 4)

    # we check the conditions on the incoming argument
    # and any existing annotation
    # we also check for consistency between both annotations
    if (
        is_consistent(arg_type.__args__[1], module_instance.num_features)
        and is_consistent(n.type.__args__[1], module_instance.num_features)
        and is_consistent(arg_type, n.type)
    ):
        # we choose the more precise type
        # to be the node type
        # so if an incoming argument has more type information
        # we set this node's type to be the argument type
        n.type = get_greatest_upper_bound(arg_type, n.type)
        return n.type
    else:
        raise TypeError(
            f"Cannot apply {module_instance} with input type {arg_type} and existing type {n.type} on {n}"
        )

