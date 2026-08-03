from typing import Any

def create_namedtuple(
    cls,
    field_value_tuples: list[tuple[str, tree_metadata.ValueMetadataEntry]],
) -> type[tuple[Any, ...]]:
  """Returns instance of a new namedtuple type structurally identical to `cls`."""
  fields, values = zip(*field_value_tuples)
  module_name, class_name = tree_rich_types._module_and_class_name(cls)  # pylint: disable=protected-access
  new_type = tree_rich_types._new_namedtuple_type(module_name, class_name, fields)  # pylint: disable=protected-access
  return new_type(*values)

