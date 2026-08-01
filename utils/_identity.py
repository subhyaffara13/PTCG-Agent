
def _identity(o: T) -> T:
    return o


def _identity(x):
    return x


def _identity(x: Any) -> Any:
    return x


def _identity(
    score: Tensor,
    batch: Tensor,
    head: Tensor,
    token_q: Tensor,
    token_kv: Tensor,
) -> Tensor:
    return score


def _identity(x):
    return x


def _identity(val: _T) -> _T:
    return val


def _identity(x, **_): return x


def _identity(x):
  return x


def _identity(x):
  return x


def _identity(x: _Tin) -> _Tin:
  """Pass through function."""
  return x

