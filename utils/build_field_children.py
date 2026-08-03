from typing import Any, Callable, Optional

def build_field_children(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    fields_or_attribute_names: Sequence[dataclasses.Field[Any] | str],
    attr_style_fn: (
        Callable[[str], part_interface.RenderableTreePart] | None
    ) = None,
) -> list[part_interface.RenderableTreePart]:
  """Renders a set of fields/attributes into a list of comma-separated children.

  This is a helper function used for rendering dataclasses, namedtuples, and
  similar objects, of the form ::

    ClassName(
        field_name_one=value1,
        field_name_two=value2,
    )

  If `fields_or_attribute_names` includes dataclass fields:

  * Metadata for the fields will be visible on hover,

  * Fields with ``repr=False`` will be hidden unless roundtrip mode is enabled.

  Args:
    node: Node to render.
    path: Path to this node.
    subtree_renderer: How to render subtrees (see `TreescopeSubtreeRenderer`)
    fields_or_attribute_names: Sequence of fields or attribute names to render.
      Any field with the metadata key "treescope_always_collapse" set to True
      will always render collapsed.
    attr_style_fn: Optional function which makes attributes to a part that
      should render them. If not provided, all parts are rendered as plain text.

  Returns:
    A list of child objects. This can be passed to
    `common_structures.build_foldable_tree_node_from_children` (with
    ``comma_separated=False``)
  """
  if attr_style_fn is None:
    attr_style_fn = basic_parts.Text

  field_names = []
  fields: list[Optional[dataclasses.Field[Any]]] = []
  for field_or_name in fields_or_attribute_names:
    if isinstance(field_or_name, str):
      field_names.append(field_or_name)
      fields.append(None)
    else:
      field_names.append(field_or_name.name)
      fields.append(field_or_name)

  children = []
  for i, (field_name, maybe_field) in enumerate(zip(field_names, fields)):
    child_path = None if path is None else f"{path}.{field_name}"

    if i < len(fields) - 1:
      # Not the last child. Always show a comma, and add a space when
      # collapsed.
      comma_after = basic_parts.siblings(
          ",", basic_parts.FoldCondition(collapsed=basic_parts.Text(" "))
      )
    else:
      # Last child: only show the comma when the node is expanded.
      comma_after = basic_parts.FoldCondition(expanded=basic_parts.Text(","))

    if maybe_field is not None:
      hide_except_in_roundtrip = not maybe_field.repr
      force_collapsed = maybe_field.metadata.get(
          "treescope_always_collapse", False
      )
    else:
      hide_except_in_roundtrip = False
      force_collapsed = False

    field_name_rendering = attr_style_fn(field_name)

    try:
      field_value = getattr(node, field_name)
    except AttributeError:
      child = basic_parts.FoldCondition(
          expanded=common_styles.CommentColor(
              basic_parts.siblings("# ", field_name_rendering, " is missing")
          )
      )
    else:
      child = basic_parts.siblings_with_annotations(
          field_name_rendering,
          "=",
          subtree_renderer(field_value, path=child_path),
      )

    child_line = basic_parts.build_full_line_with_annotations(
        child, comma_after
    )
    if force_collapsed:
      layout_algorithms.expand_to_depth(child_line, 0)
    if hide_except_in_roundtrip:
      child_line = basic_parts.RoundtripCondition(roundtrip=child_line)

    children.append(child_line)

  return children

