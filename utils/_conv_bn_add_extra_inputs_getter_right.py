
def _conv_bn_add_extra_inputs_getter_right(pattern):
    """get inputs pattern for extra inputs, inputs for root node
    are assumed to be copied over from root node to the fused node
    """
    _, extra_input, _bn_conv = pattern
    return [extra_input]

