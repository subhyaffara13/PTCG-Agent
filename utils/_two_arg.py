
def _two_arg(f):
    @_wraps(f)
    def _f(x1, x2, /, **kwargs):
        x1, x2 = _fix_promotion(x1, x2)
        return f(x1, x2, **kwargs)
    if _f.__doc__ is None:
        _f.__doc__ = f"""\
Array API compatibility wrapper for torch.{f.__name__}.

See the corresponding PyTorch documentation and/or the array API specification
for more details.

"""
    return _f

