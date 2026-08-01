
def same_dtype(match):
    return match.output_node().args[0].meta["val"].dtype == match.kwargs["dtype"]


def same_dtype(*args, **kwargs):
    """
    When the dtype is the same, return the original ShardedTensor.

    Args: same as ``torch.Tensor.type_as``.

    Return (bool): Whether to return early or not.
    """
    return args[0].dtype == args[1].dtype

