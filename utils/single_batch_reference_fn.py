
def single_batch_reference_fn(input, parameters, module):
    """Reference function for modules supporting no batch dimensions.

    The module is passed the input and target in batched form with a single item.
    The output is squeezed to compare with the no-batch input.
    """
    def unsqueeze_inp(inp):
        if isinstance(inp, (list, tuple)):
            return [t.unsqueeze(0) for t in inp]
        return inp.unsqueeze(0)

    single_batch_input = unsqueeze_inp(input)
    single_batch_input = [single_batch_input] if isinstance(single_batch_input, torch.Tensor) else single_batch_input
    with freeze_rng_state():
        return module(*single_batch_input).squeeze(0)

