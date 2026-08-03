from typing import Any

def register_dtype_kind(dtype: Any, kind: int):
  _dtype_to_dtype_kind[dtype] = kind
  _dtype_kind_to_dtype[kind] = dtype

