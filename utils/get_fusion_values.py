from typing import Callable

def get_fusion_values(
    fusion: Callable, *args, **kwargs
) -> tuple[
    Callable, tuple[typing.SupportsShape, ...], tuple[typing.SupportsShape, ...]
]:
  return _get_fusion_values(fusion, args, kwargs)

