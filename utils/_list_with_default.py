
def _list_with_default(out_size: list[int], defaults: list[int]) -> list[int]:
    import torch

    if isinstance(out_size, (int, torch.SymInt)):
        return out_size
    if len(defaults) <= len(out_size):
        raise ValueError(f"Input dimension should be at least {len(out_size) + 1}")
    return [
        v if v is not None else d
        for v, d in zip(out_size, defaults[-len(out_size) :], strict=False)
    ]

