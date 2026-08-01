
def _conv_bn_add_extra_inputs_getter_left(add_pattern):
    """get inputs pattern for extra inputs, inputs for root node
    are assumed to be copied over from root node to the fused node
    """
    _, _bn_conv, extra_input = add_pattern
    return [extra_input]

