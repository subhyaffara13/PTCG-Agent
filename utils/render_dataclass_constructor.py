from typing import Any

def render_dataclass_constructor(
    node: Any,
) -> part_interface.RenderableTreePart:
  """Renders the constructor for a dataclass, including the open parenthesis."""
  assert dataclasses.is_dataclass(node) and not isinstance(node, type)
  if not dataclass_util.init_takes_fields(type(node)):
    constructor_open = basic_parts.siblings(
        basic_parts.RoundtripCondition(
            roundtrip=basic_parts.Text(
                "treescope.dataclass_util.dataclass_from_attributes("
            )
        ),
        common_structures.maybe_qualified_type_name(type(node)),
        basic_parts.RoundtripCondition(
            roundtrip=basic_parts.Text(", "),
            not_roundtrip=basic_parts.Text("("),
        ),
    )
  else:
    constructor_open = basic_parts.siblings(
        common_structures.maybe_qualified_type_name(type(node)), "("
    )
  return constructor_open

