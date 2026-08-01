
def conv_backwards(
    grad_output: list[int],
    input: list[int],
    weight: list[int],
    biases: Optional[list[int]],
):
    # Bias gradient is always generated regardess of if biases is supplied
    return _copy(input), _copy(weight), [grad_output[1]]

