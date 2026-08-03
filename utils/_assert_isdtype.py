from typing import Any

def _assert_isdtype(dtype: Any) -> None:
  if not isinstance(dtype, DType):
    raise TypeError('etils DTypes can only be compared with other etils')

