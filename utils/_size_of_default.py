
def _size_of_default(num_bytes: int | torch.SymInt) -> int:
    return optimization_hint(num_bytes)

