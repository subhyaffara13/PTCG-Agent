
def set_warn_on_accumulate_grad_stream_mismatch(enabled: bool) -> None:
    """Whether to warn when the AccumulateGrad node's stream does not match the stream
    of the node that produced the incoming gradient.
    """
    return torch._C._set_warn_on_accumulate_grad_stream_mismatch(enabled)

