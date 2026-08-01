
def _new_namedtuple_type(
    module_name: str,
    class_name: str,
    fields: Sequence[str],
) -> Type[tuple[Any, ...]]:
  """Returns a namedtuple type created in the current module.

  NOTE: `module_name` and `class_name` are concatenated to create a unique
  class name to avoid name collisions.

  Args:
    module_name: Module name of original namedtuple saved in metadata.
    class_name: Class name of original namedtuple saved in metadata.
    fields: The fields of the namedtuple.
  """
  # TODO: b/365169723 - Return concrete NamedTuple if available in given module.
  arity = len(fields)
  unique_class_name = f'{module_name}_{class_name}_{arity}'
  # Valid class name must not contain dots.
  valid_class_name = unique_class_name.replace('.', '_')
  return collections.namedtuple(valid_class_name, fields)

