
def _conv_add_relu_extra_inputs_getter_right(pattern):
    """get inputs pattern for extra inputs, inputs for root node
    are assumed to be copied over from root node to the fused node
    """
    _relu, add_pattern = pattern
    _, extra_input, _conv = add_pattern
    return [extra_input]

