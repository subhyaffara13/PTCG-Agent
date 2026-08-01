
def _conv_add_extra_inputs_getter_left(pattern):
    """get inputs pattern for extra inputs, inputs for root node
    are assumed to be copied over from root node to the fused node
    """
    _, _conv, extra_input = pattern
    return [extra_input]

