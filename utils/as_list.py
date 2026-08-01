
def as_list(
    x: list[object] | object,
    # pyre-fixme[11]: Annotation `immutable_list` is not defined as a type.
) -> list[object] | torch.fx.immutable_collections.immutable_list:  # type: ignore[valid-type]
    # During tracing, `aten.sum.dim_IntList` uses `immutable_list` for its args,
    # which is an object but treated as a list by the tracer. Therefore, keep
    # `immutable_list` intact here as well.
    if type(x) is list or isinstance(x, torch.fx.immutable_collections.immutable_list):
        return x
    else:
        return [x]


def as_list(x, keep_none):
    if type(x) is list:
        return x
    elif type(x) is np.ndarray:
        return list(x)
    elif keep_none and x is None:
        return None
    else:
        return [x]

