from typing import Callable

def collate_numpy_scalar_fn(
    batch,
    *,
    collate_fn_map: dict[type | tuple[type, ...], Callable] | None = None,
):
    return torch.as_tensor(batch)

