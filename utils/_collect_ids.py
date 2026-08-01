
def _collect_ids(ctx: Context) -> frozenset[int]:
  """Collects all object ids from the context and its options.

  This function traverses the context object and all its attributes. This is
  used to freeze the context and all its options, so that they cannot be
  modified after the context is entered.

  Args:
    ctx: The context object to collect ids from.

  Returns:
    A frozenset of all object ids from the context and its options.
  """
  ids = {id(ctx)}

  def _traverse(obj: typing.Any) -> None:
    if id(obj) in ids:
      return
    if dataclasses.is_dataclass(obj):
      ids.add(id(obj))
      for field in dataclasses.fields(obj):
        _traverse(getattr(obj, field.name))
    elif isinstance(obj, (list, tuple, set)):
      for item in obj:
        _traverse(item)
    elif isinstance(obj, dict):
      for value in obj.values():
        _traverse(value)

  for obj in vars(ctx).values():
    _traverse(obj)
  return frozenset(ids)

