
def try_real_annotations(fn, loc):
    """Try to use the Py3.5+ annotation syntax to get the type."""
    try:
        # Note: anything annotated as `Optional[T]` will automatically
        # be returned as `Union[T, None]` per
        # https://github.com/python/cpython/blob/main/Lib/typing.py#L732
        sig = inspect.signature(fn)
    except ValueError:
        return None

    all_annots = [sig.return_annotation] + [
        p.annotation for p in sig.parameters.values()
    ]
    if all(ann is sig.empty for ann in all_annots):
        return None

    arg_types = [ann_to_type(p.annotation, loc) for p in sig.parameters.values()]
    return_type = ann_to_type(sig.return_annotation, loc)
    return arg_types, return_type

