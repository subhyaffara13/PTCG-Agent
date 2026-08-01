
def _get_orig_buffer_dtypes(
    state: _FSDPState,
    buffer_names: list[str],
) -> list[torch.dtype]:
    """
    Returns the original buffer types of the given buffer names.
    """
    buffer_dtypes: list[torch.dtype] = []
    for buffer_name in buffer_names:
        _p_assert(
            buffer_name in state._buffer_name_to_orig_dtype,
            f"{buffer_name} is missing from pre-computed dict on rank "
            f"{state.rank}, which only has keys "
            f"{state._buffer_name_to_orig_dtype.keys()}",
        )
        buffer_dtypes.append(state._buffer_name_to_orig_dtype[buffer_name])
    return buffer_dtypes

