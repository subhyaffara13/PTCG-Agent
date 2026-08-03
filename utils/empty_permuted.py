from typing import Any

def empty_permuted(
    size: list[int | torch.SymInt],
    physical_layout: list[int],
    **kwargs: Any,
) -> torch.Tensor:
    is_identity = list(physical_layout) == list(range(len(physical_layout)))

    if is_identity:
        return torch.empty(size, **kwargs)
    else:
        perm = [0] * len(size)
        for p, l in enumerate(physical_layout):
            perm[l] = p
        return torch.empty([size[l] for l in physical_layout], **kwargs).permute(perm)


def empty_permuted(
    shape,
    physical_layout,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    return prims.empty_permuted(
        shape,
        physical_layout,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )

