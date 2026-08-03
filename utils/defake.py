from typing import Any

def defake(x: Any) -> Any:
    if not isinstance(x, FakeTensor):
        return x
    size: torch._prims_common.ShapeType
    stride: torch._prims_common.StrideType
    if x._has_symbolic_sizes_strides:
        # optimization_hint is appropriate here because defake only needs a
        # plausible concrete shape to allocate a real tensor; it does not need
        # to install guards. For unbacked symbols the heuristic fallback is fine.
        size = [
            torch.fx.experimental.symbolic_shapes.optimization_hint(s) for s in x.size()
        ]
        stride = [
            torch.fx.experimental.symbolic_shapes.optimization_hint(s)
            for s in x.stride()
        ]
    else:
        size = x.size()
        stride = x.stride()
    y = torch.empty_strided(
        size,
        stride,
        dtype=x.dtype,
        device=x.device,
        requires_grad=x.requires_grad,
    )
    y.zero_()
    return y

