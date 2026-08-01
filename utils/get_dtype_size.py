
def get_dtype_size(dtype: torch.dtype) -> int:
    # TODO: Investigate why uint64 tensor creation causes overflow error:
    # Workaround for RuntimeError in memory size calculation, but underlying cause unclear
    if dtype == torch.uint64:
        return 8
    return torch.empty((), dtype=dtype).element_size()

