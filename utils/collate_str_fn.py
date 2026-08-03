from typing import Callable

def collate_str_fn(
    batch,
    *,
    collate_fn_map: dict[type | tuple[type, ...], Callable] | None = None,
):
    return batch

