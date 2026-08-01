
def split_result_tensors(
    result: torch.Tensor, inputs: list[torch.Tensor]
) -> tuple[torch.Tensor, ...]:
    """
    A free function for use in the merge_matmul graph transformation below that
    splits the output from a merged matmul into the individual results for each
    input tensor.

    Arguments:
        result: The merged matmul result tensor.
        inputs: The list of inputs that were merged into one for the matmul.

    Returns:
        List of matmul results for each input tensor.
    """
    # When fx tracer is running, x.shape[0] will be torch.fx.Attribute but we
    # need an int even when tracing
    if isinstance(result, torch.fx.Proxy):
        splits = [0] * len(inputs)
    else:
        splits = [x.shape[0] for x in inputs]

    return torch.split(result, splits)

