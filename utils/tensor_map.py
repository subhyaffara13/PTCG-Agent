from typing import Callable

def tensor_map(tensor: Tensor, cb: Callable[[int, Tensor], Tensor | None]) -> Tensor:
    """
    Transforms a tensor by mapping a callback over the current rank and its
    local shard.

    Under LocalTensorMode, calls cb(rank, shard) for each simulated rank and
    returns a LocalTensor. In real distributed (no LocalTensorMode), calls
    cb(dist.get_rank(), tensor) and returns the result directly.
    """
    lm = enabled_local_tensor_mode()
    if lm is not None:
        if not isinstance(tensor, LocalTensor):
            raise AssertionError(f"Expected LocalTensor, got {type(tensor)}")
        return lm.tensor_map(tensor, cb)
    else:
        r = cb(dist.get_rank(), tensor)
        if r is None:
            raise AssertionError("callback returned None")
        return r

