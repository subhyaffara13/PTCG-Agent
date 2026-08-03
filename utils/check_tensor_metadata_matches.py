from typing import Callable

def check_tensor_metadata_matches(
    nv: torch.Tensor, rv: torch.Tensor, desc: Callable[[], str]
) -> None:
    if not callable(desc):
        raise AssertionError(f"desc must be callable, got {type(desc)}")
    if nv.size() != rv.size():
        raise AssertionError(f"{desc()}: sizes {nv.size()} != {rv.size()}")
    if nv.dtype != rv.dtype:
        raise AssertionError(f"{desc()}: dtype {nv.dtype} != {rv.dtype}")
    same_strides, idx = torch._prims_common.check_significant_strides(
        nv, rv, only_cuda=False
    )
    if not same_strides:
        raise AssertionError(
            f"{desc()}: strides {nv.stride()} != {rv.stride()} (mismatch at index {idx})"
        )

