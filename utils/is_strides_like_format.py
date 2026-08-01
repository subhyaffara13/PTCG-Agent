
def is_strides_like_format(func, *args, **kwargs):
    data = _get_data(args[0])
    if data.is_sparse:
        raise ValueError(
            "MaskedTensors with sparse data do not have is_strides_like_format"
        )
    return func(data, *args[1:], **kwargs)

