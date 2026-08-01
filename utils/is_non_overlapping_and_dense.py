
def is_non_overlapping_and_dense(func, *args, **kwargs):
    data = _get_data(args[0])
    if data.is_sparse:
        raise ValueError(
            "MaskedTensors with sparse data do not have is_non_overlapping_and_dense"
        )
    return func(data, *args[1:], **kwargs)

