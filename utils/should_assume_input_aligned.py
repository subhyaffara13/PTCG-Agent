
def should_assume_input_aligned(example_input: torch.Tensor) -> bool:
    # See Note: [Input Alignment handling in Inductor]

    # right now, we only care about alignment for cuda tensors.
    if not is_gpu(example_input.device.type):
        return False
    return config.assume_aligned_inputs or tensor_is_aligned(example_input)

