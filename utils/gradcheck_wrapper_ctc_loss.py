
def gradcheck_wrapper_ctc_loss(op, input, *args, **kwargs):
    """Gradcheck wrapper for ctc loss to project onto log-simplex space."""
    # See https://github.com/pytorch/pytorch/issues/52241
    return op(input.log_softmax(dim=2), *args, **kwargs)

