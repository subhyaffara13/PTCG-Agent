from typing import Callable

def rank_map(cb: Callable[[int], Tensor]) -> Tensor:
    """
    Creates a tensor by mapping a callback over the current rank.

    Under LocalTensorMode, calls cb(rank) for each simulated rank and returns
    a LocalTensor. In real distributed (no LocalTensorMode), calls
    cb(dist.get_rank()) and returns a plain Tensor.
    """
    lm = enabled_local_tensor_mode()
    if lm is not None:
        return lm.rank_map(cb)
    else:
        return cb(dist.get_rank())

