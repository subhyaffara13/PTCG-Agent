
def set_value(ctx: click.Context, key: Any, value: Any) -> None:
    """
    Store the given key/value.

    This doesn't follow symlinks, to avoid accidentally modifying a file at a
    potentially untrusted path.
    """

    file = ctx.obj["FILE"]
    quote = ctx.obj["QUOTE"]
    export = ctx.obj["EXPORT"]
    success, key, value = set_key(file, key, value, quote, export)
    if success:
        click.echo(f"{key}={value}")
    else:
        sys.exit(1)


def set_value(value):
    VALUE_FUTURE.set_result(value)


def set_value(
    config_path: str,
    config: Any,
    value: Any,
    *,
    accept_new_attributes: bool = False,
):
  """Sets value of field described by config_path.

  Example usage:
    >>> config = {'a': {'b', {'c', 10}}}
    >>> config_path.set_value('a.b.c', config, 20)
    >>> assert config['a']['b']['c'] == 20

  Args:
    config_path: Any string that `split` can process.
    config: A nested datastructure
    value: A value to assign to final field.
    accept_new_attributes: If `True`, the new config attributes can be added

  Raises:
    IndexError: Integer field not found in nested structure.
    KeyError: Non-integer field not found in nested structure.
    ValueError: Empty/invalid config_path after parsing.
  """
  holder, field = _get_holder_field(config_path, config)

  if isinstance(field, int) and isinstance(holder, MutableSequence):
    holder[field] = value
  elif hasattr(holder, '__setitem__') and (
      field in holder or accept_new_attributes
  ):
    holder[field] = value
  elif hasattr(holder, str(field)):
    setattr(holder, str(field), value)
  else:
    if isinstance(field, int):
      raise IndexError(
          f'{field} is not a valid index for {type(holder)} '
          f'(in: {config_path})')
    raise KeyError(f'{field} is not a valid key or attribute of {type(holder)} '
                   f'(in: {config_path})')

