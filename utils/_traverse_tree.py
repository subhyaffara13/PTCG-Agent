
def _traverse_tree(path, obj, *, update_fn=None, cond_fn=None):
  """Helper function for ``Cursor.apply_update`` and ``Cursor.find_all``.
  Exactly one of ``update_fn`` and ``cond_fn`` must be not None.

  - If ``update_fn`` is not None, then ``Cursor.apply_update`` is calling
    this function and ``_traverse_tree`` will return a generator where
    each generated element is of type Tuple[Tuple[Union[str, int], AccessType], Any].
    The first element is a tuple of the key path and access type where the
    change was applied from the ``update_fn``, and the second element is
    the newly modified value. If the generator is non-empty, then the
    tuple key path will always be non-empty as well.
  - If ``cond_fn`` is not None, then ``Cursor.find_all`` is calling this
    function and ``_traverse_tree`` will return a generator where each
    generated element is of type Tuple[Union[str, int], AccessType]. The
    tuple contains the key path and access type where the object was found
    that fulfilled the conditions of the ``cond_fn``.
  """
  if not (bool(update_fn) ^ bool(cond_fn)):
    raise TraverseTreeError(update_fn, cond_fn)

  if path:
    str_path = '/'.join(str(key) for key, _ in path)
    if update_fn:
      new_obj = update_fn(str_path, obj)
      if new_obj is not obj:
        yield path, new_obj
        return
    elif cond_fn(str_path, obj):  # type: ignore
      yield path
      return

  if isinstance(obj, (FrozenDict, dict)):
    items = obj.items()
    access_type = AccessType.ITEM
  elif is_named_tuple(obj):
    items = ((name, getattr(obj, name)) for name in obj._fields)  # type: ignore
    access_type = AccessType.ATTR
  elif isinstance(obj, (list, tuple)):
    items = enumerate(obj)
    access_type = AccessType.ITEM
  elif dataclasses.is_dataclass(obj):
    items = (
      (f.name, getattr(obj, f.name)) for f in dataclasses.fields(obj) if f.init
    )
    access_type = AccessType.ATTR
  else:
    return

  if update_fn:
    for key, value in items:
      yield from _traverse_tree(
        path + ((key, access_type),), value, update_fn=update_fn
      )
  else:
    for key, value in items:
      yield from _traverse_tree(
        path + ((key, access_type),), value, cond_fn=cond_fn
      )

