from typing import Callable

def collate_float_fn(
    batch,
    *,
    collate_fn_map: dict[type | tuple[type, ...], Callable] | None = None,
):
    return torch.tensor(batch, dtype=torch.float64)

