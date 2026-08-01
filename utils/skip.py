
def Skip(self: JpegImageFile, marker: int) -> None:
    assert self.fp is not None
    n = i16(self.fp.read(2)) - 2
    ImageFile._safe_read(self.fp, n)


def skip(fn: Callable[_P, _R] | None = None) -> Callable[..., Any]:
    """
    Skip frames associated with the function code, but still process recursively
    invoked frames
    """
    if fn is None:
        return skip
    fn = innermost_fn(fn)
    assert callable(fn)
    skip_code(fn.__code__)
    fn._torchdynamo_disable = True  # type: ignore[attr-defined]
    return fn


def skip(op_name, variant_name='', *, device_type=None, dtypes=None):
    return (op_name, variant_name, device_type, dtypes, False)


def skip(op_name, variant_name="", *, device_type=None, dtypes=None):
    return (op_name, variant_name, device_type, dtypes, False)


def skip(message, **kwargs):
    def skipper(test):
        if all(value == getattr(test, attr) for attr, value in kwargs.items()):
            return message
    return skipper

