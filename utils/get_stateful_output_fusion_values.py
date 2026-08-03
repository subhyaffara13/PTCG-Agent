from typing import Callable

def get_stateful_output_fusion_values(
    fusion: Callable,
    *args,
    **kwargs,
):
  return _get_fusion_values(
      fusion, args, kwargs, discharge_refs=True, allow_additional_outputs=True)

