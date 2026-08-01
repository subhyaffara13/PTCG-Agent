
def with_metadata(
  initializer: F,
  on_set_value: tp.Union[SetValueHook[A], tp.Sequence[SetValueHook[A]]] = (),
  on_get_value: tp.Union[SetValueHook[A], tp.Sequence[SetValueHook[A]]] = (),
  on_create_value: tp.Union[
    CreateValueHook[A], tp.Sequence[CreateValueHook[A]]
  ] = (),
  on_add_axis: tp.Union[
    AddAxisHook[Variable[A]], tp.Sequence[AddAxisHook[Variable[A]]]
  ] = (),
  on_remove_axis: tp.Union[
    RemoveAxisHook[Variable[A]],
    tp.Sequence[RemoveAxisHook[Variable[A]]],
  ] = (),
  **metadata: tp.Any,
) -> F:
  if on_set_value or on_get_value or on_create_value or on_add_axis or on_remove_axis:
    warnings.warn(
      'Variable hooks are deprecated in favor of users creating their own '
      'Variable types and overloading `get_value` and `set_value` instead.'
    )

  if on_set_value:
    if callable(on_set_value):
      on_set_value = (on_set_value,)
    else:
      on_set_value = tuple(on_set_value)
  else:
    on_set_value = ()

  if on_get_value:
    if callable(on_get_value):
      on_get_value = (on_get_value,)
    else:
      on_get_value = tuple(on_get_value)
  else:
    on_get_value = ()

  if on_create_value:
    if callable(on_create_value):
      on_create_value = (on_create_value,)
    else:
      on_create_value = tuple(on_create_value)
  else:
    on_create_value = ()

  if on_add_axis:
    if callable(on_add_axis):
      on_add_axis = (on_add_axis,)
    else:
      on_add_axis = tuple(on_add_axis)
  else:
    on_add_axis = ()

  if on_remove_axis:
    if callable(on_remove_axis):
      on_remove_axis = (on_remove_axis,)
    else:
      on_remove_axis = tuple(on_remove_axis)
  else:
    on_remove_axis = ()

  @functools.wraps(initializer)
  def wrapper(*args):
    return VariableMetadata(
      initializer(*args),
      on_set_value=on_set_value,
      on_get_value=on_get_value,
      on_create_value=on_create_value,
      on_add_axis=on_add_axis,
      on_remove_axis=on_remove_axis,
      metadata=metadata,
    )

  return wrapper  # type: ignore

