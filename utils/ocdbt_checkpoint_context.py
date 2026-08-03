import copy
from typing import Any

def ocdbt_checkpoint_context(use_ocdbt: bool, ts_context: Any):
  """Use OCDBT driver within context."""
  original_type_handlers = copy.deepcopy(
      type_handler_registry._DEFAULT_TYPE_HANDLERS
  )
  if use_ocdbt:
    type_handler_registry.register_standard_handlers_with_options(
        use_ocdbt=use_ocdbt, ts_context=ts_context
    )
  try:
    yield
  finally:
    for original_type, original_handler in original_type_handlers:
      type_handler_registry.GLOBAL_TYPE_HANDLER_REGISTRY.add(
          original_type, original_handler, override=True
      )

