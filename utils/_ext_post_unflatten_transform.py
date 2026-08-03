from typing import Any

def _ext_post_unflatten_transform(
    tensor: torch.Tensor,
    param_extension: Any,
    fsdp_extension: FSDPExtensions | None = None,
) -> torch.Tensor:
    if fsdp_extension is not None and param_extension is not None:
        return fsdp_extension.post_unflatten_transform(tensor, param_extension)
    return tensor

