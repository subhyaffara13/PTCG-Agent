from typing import Callable

def get_stateful_input_fusion_values(
    fusion: Callable,
    *args,
    **kwargs,
):
  return _get_fusion_values(fusion, args, kwargs, discharge_refs=True)

