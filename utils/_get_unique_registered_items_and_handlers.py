
def _get_unique_registered_items_and_handlers(
    registry: handler_registration.CheckpointHandlerRegistry,
) -> List[Tuple[str, CheckpointHandler]]:
  """Returns unique items and handlers from the registry.

  Args:
    registry: The registry to get the items and handlers from.

  Returns:
    A list of unique `(item name, handler)` tuples.
  """
  item_and_handers = []
  for (
      item,
      _,
  ), handler in registry.get_all_entries().items():
    if item is not None and (item, handler) not in item_and_handers:
      item_and_handers.append((item, handler))
  return item_and_handers

