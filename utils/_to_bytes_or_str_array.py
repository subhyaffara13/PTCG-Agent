
def _to_bytes_or_str_array(result, output_dtype_like):
    """
    Helper function to cast a result back into an array
    with the appropriate dtype if an object array must be used
    as an intermediary.
    """
    output_dtype_like = np.asarray(output_dtype_like)
    if result.size == 0:
        # Calling asarray & tolist in an empty array would result
        # in losing shape information
        return result.astype(output_dtype_like.dtype)
    ret = np.asarray(result.tolist())
    if isinstance(output_dtype_like.dtype, np.dtypes.StringDType):
        return ret.astype(type(output_dtype_like.dtype))
    return ret.astype(type(output_dtype_like.dtype)(_get_num_chars(ret)))

