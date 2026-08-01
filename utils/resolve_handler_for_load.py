
def resolve_handler_for_load(
    registry: CheckpointableHandlerRegistry,
    abstract_checkpointable: Any | None,
    *,
    name: str,
    handler_typestr: str | None = None,
) -> CheckpointableHandler:
  """Resolves a :py:class:`~.v1.handlers.CheckpointableHandler` for loading.

    1. If `abstract_checkpointable` is a `StatefulCheckpointable`, prefer the
       handler matching `handler_typestr` if it is handleable.
    2. If `name` is explicitly registered, return its handler (provided it is
       handleable or `abstract_checkpointable` is `None`).
    3. If `handler_typestr` matches a registered handler, return it (provided it
       is handleable or `abstract_checkpointable` is `None`).
    4. If `abstract_checkpointable` is provided, return the most recently
       registered handler that can handle it.
    5. Fallback to the explicitly registered handler for `name` even if
       incompatible, otherwise raise `NoEntryError`.

  Args:
    registry: The
      :py:class:`~.v1.handlers.registration.CheckpointableHandlerRegistry` to
      search.
    abstract_checkpointable: An abstract checkpointable to resolve.
    name: The name of the checkpointable.
    handler_typestr: A :py:class:`~.v1.handlers.CheckpointableHandler` typestr
      to guide resolution. We allow a None value for handler_typestr as its
      possible to find the last registered handler given a specified
      abstract_checkpointable.

  Returns:
    A :py:class:`~.v1.handlers.CheckpointableHandler` instance.

  Raises:
    NoEntryError: If no compatible
    :py:class:`~.v1.handlers.CheckpointableHandler`
    can be found.
  """
  explicit_handler = (
      _construct_handler_instance(name, registry.get(name))
      if registry.has(name)
      else None
  )

  def is_handleable(handler: CheckpointableHandler, ckpt: Any) -> bool | None:
    return handler.is_abstract_handleable(ckpt)

  # Find the handler matching the typestr from the checkpoint metadata.
  resolved_by_typestr = None
  if handler_typestr:
    for h_type, ckpt_name in reversed(registry.get_all_entries()):
      h_type_str = handler_types.typestr(h_type)
      secondary_typestrs = registry.get_secondary_typestrs(h_type)
      if h_type_str == handler_typestr or handler_typestr in secondary_typestrs:
        resolved_by_typestr = _construct_handler_instance(ckpt_name, h_type)
        break

  if handler_typestr and not resolved_by_typestr:
    logging.warning(
        'No handler found for typestr %s (or its converted form). The '
        'checkpointable may be restored with different handler logic '
        'than was used for saving.',
        handler_typestr,
    )

  # Determine if we're in a "stateful" context.
  is_stateful = False
  if abstract_checkpointable is not None:
    is_stateful = isinstance(
        abstract_checkpointable, handler_types.StatefulCheckpointable
    )

  # 1. If stateful, prefer the stateful handler over explicit name.
  if is_stateful and resolved_by_typestr:
    if is_handleable(resolved_by_typestr, abstract_checkpointable):
      return resolved_by_typestr

  # 2. Explicitly registered handler.
  if explicit_handler:
    if abstract_checkpointable is None or is_handleable(
        explicit_handler, abstract_checkpointable
    ):
      return explicit_handler

  # 3. Any handler matching the typestr.
  if resolved_by_typestr:
    if abstract_checkpointable is None or is_handleable(
        resolved_by_typestr, abstract_checkpointable
    ):
      return resolved_by_typestr

  # 4. Any handler that can handle the object.
  if abstract_checkpointable is not None:
    possible_handlers = _get_possible_handlers(
        registry, is_handleable, abstract_checkpointable
    )
    if possible_handlers:
      return possible_handlers[-1]

  # 5. Fallback: Return explicit handler even if incompatible.
  if explicit_handler:
    return explicit_handler

  raise NoEntryError(
      f'No entry for checkpointable={name} in the registry, using'
      f' handler_typestr={handler_typestr} and'
      f' abstract_checkpointable={abstract_checkpointable}. Registry contents:'
      f' {registry.get_all_entries()}'
  )

