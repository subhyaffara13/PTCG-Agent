
def init_takes_fields(cls: type[Any]) -> bool:
  """Returns True if ``cls.__init__`` takes exactly one argument per field.

  This is a heuristic for determining whether this dataclass can be rebuilt
  from its attributes using a simple repr-like format (e.g.
  ``Foo(bar=1, baz=2)``) or whether safely rebuilding it requires using
  :func:`dataclass_from_attributes` above. This is used during pretty-printing
  to determine whether to switch to a more verbose form when a round-trippable
  representation is requested.

  Note that it's technically possible to override ``__init__`` so that it takes
  the fields as attributes and then modifies them; it's not really possible to
  check for this, so we just check that the signature looks correct.

  Args:
    cls: The dataclass to check.
  """
  assert dataclasses.is_dataclass(cls)
  fields = dataclasses.fields(cls)
  remaining_field_set = set(field.name for field in fields)
  signature = inspect.signature(cls.__init__)

  # Skip `self` argument.
  parameters = list(signature.parameters.values())
  for parameter in parameters[1:]:
    if parameter.kind not in {
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY,
    }:
      # It might not be safe to pass keyword arguments.
      return False
    if parameter.name in remaining_field_set:
      remaining_field_set.remove(parameter.name)
    else:
      # Unexpected parameter; this means __init__ was overridden with extra
      # parameters.
      return False

  if remaining_field_set:
    # Some fields were not present in __init__!
    return False
  else:
    return True

