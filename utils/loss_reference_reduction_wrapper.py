
def loss_reference_reduction_wrapper(fn):
    def wrapper(input, target, *, size_average=None, reduce=None, reduction="mean", **other_kwargs):
        if size_average is not None or reduce is not None:
            raise RuntimeError(
                "The keyword arguments 'size_average' and 'reduce' are deprecated and not supported by this wrapper"
            )
        output = fn(input, target, **other_kwargs)
        if reduction == "mean":
            return np.mean(output)
        elif reduction == "sum":
            return np.sum(output)
        else:  # reduction == "none"
            return output

    return wrapper

