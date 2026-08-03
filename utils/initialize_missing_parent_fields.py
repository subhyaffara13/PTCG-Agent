from typing import Any

def initialize_missing_parent_fields(
    config: Any, override: str,
    allowed_missing: Sequence[str]):
  """Adds some missing nested holder fields for a particular override.

  For example if override is 'config.a.b.c' and config.a is None, it
  will default initialize config.a, and if config.a.b is None will default
  initialize it as well. Only overrides present in allowed_missing will
  be initialized.

  Args:
    config: config object (typically dataclass)
    override: dot joined override name.
    allowed_missing: list of overrides that are allowed
    to be set. For example, if override is 'a.b.c.d',
    allowed_missing could be ['a.b.c', 'a', 'foo.bar'].

  Raises:
    ValueError: if parent field is not of dataclass type.
  """
  fields = split(override)
  # Collect the tree levels at which we are alloed to create override
  allowed_levels = {len(split(x)) for x in allowed_missing if
                    override.startswith(x + '.')}
  child = config
  for level, f in enumerate(fields[:-1], 1):
    parent = child
    child = _get_item_or_attribute(parent, f, override)
    if child is not None:
      continue
    # Field is not yet present, see if we should create it instead.
    field_type = get_type(f, parent)
    # Note: these two assertions below are mostly guard
    # rails to prevent behaviors that might be confusing/accidental.
    # Specifically we disallow implicit creation of parent fields,
    # creating non dataclass objects. They can be revisited
    # in the future.
    if not dc.is_dataclass(field_type):
      raise ValueError(
          f'Override {override} can not be applied because '
          f'field "{f}" is None, and its type "{field_type}" is not a '
          f'dataclass in the parent of type "{type(parent)}".')

    if level not in allowed_levels:
      raise ValueError(
          f'Flag {override} can not be applied because '
          f'field "{f}" is None by default and it is not explicitly '
          'provided in flags (it can be default intialized by '
          f'providing --<path-to-{f}>.{f}=build flag')
    try:
      child = field_type()
    except Exception as e:
      raise ValueError(
          f'Override {override} can not be applied because '
          f'field "{f}" of type {field_type} can not be default instantiated:'
          f'{e}') from e
    set_value(f, parent, child)

