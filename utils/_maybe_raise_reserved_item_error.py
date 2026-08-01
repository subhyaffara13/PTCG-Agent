
def _maybe_raise_reserved_item_error(item_name: str):
  if item_name in RESERVED_ITEM_NAMES:
    raise ValueError(f'Cannot specify reserved item name: "{item_name}".')

