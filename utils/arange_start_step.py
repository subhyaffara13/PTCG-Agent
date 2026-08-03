from typing import Any
import math


def arange_start_step(
    start: number, end: number, step: number, inp0: Any, inp1: Any, inp2: Any, inp3: Any
):
    if step == 0:
        raise AssertionError("step must not be zero")
    if step < 0:
        if start < end:
            raise AssertionError(
                f"Expected start ({start}) >= end ({end}) when step < 0"
            )
    else:
        if end < start:
            raise AssertionError(
                f"Expected end ({end}) >= start ({start}) when step > 0"
            )
    return [int(math.ceil((end - start) / step))]


def arange_start_step(
    start,
    end,
    step=1,
    *,
    dtype=None,
    device=None,
    layout=None,
    pin_memory=None,
    requires_grad=False,
):
    assert dtype is not None
    length = ceildiv(end - start, step)
    return iota(
        length,
        start=start,
        step=step,
        dtype=dtype,
        device=device if device is not None else "cpu",
        requires_grad=requires_grad,
    )

