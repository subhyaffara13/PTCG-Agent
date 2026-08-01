
def _noop(_dist: Distribution, val: _T) -> _T:
    return val


def _noop(*args, return_value: _T, **kwargs) -> _T:
  del args, kwargs
  return return_value


def _noop(obj):
    return obj

