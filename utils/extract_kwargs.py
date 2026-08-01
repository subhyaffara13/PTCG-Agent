
def extract_kwargs(arg):
    kwargs = {
        "offsets": arg.offsets(),
        "lengths": arg.lengths(),
        "_metadata_cache": arg._metadata_cache,
        "_ragged_idx": arg._ragged_idx,
    }
    return kwargs

