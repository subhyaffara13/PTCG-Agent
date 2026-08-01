
def render_enumlike_item(
    object_type: type[Any],
    item_name: str,
    item_value: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
):
  """Renders a value of an enum-like type (e.g. like `enum.Enum`).

  This method can be used to render a value of a type that acts like a Python
  enum, in that there is a finite set of possible instances of the type, each of
  which have a name and a value, and where the instance can be accessed as an
  attribute (e.g. ``mytype.FOO`` is an instance of ``mytype`` with name "FOO").

  Args:
    object_type: The type of the object.
    item_name: The name of the item.
    item_value: The value of the item (``{object_type}.{item_name}.value``).
    path: The path to the object. When `render_object_constructor` is called
      from `__treescope_repr__`, this should come from the `path` argument to
      `__treescope_repr__`.
    subtree_renderer: The renderer to use to render subtrees. When
      `render_object_constructor` is called from `__treescope_repr__`, this
      should come from the `subtree_renderer` argument to `__treescope_repr__`.

  Returns:
    A rendering of the object, suitable for returning from `__treescope_repr__`.
  """
  del subtree_renderer
  return rendering_parts.build_one_line_tree_node(
      rendering_parts.siblings_with_annotations(
          rendering_parts.maybe_qualified_type_name(object_type),
          "." + item_name,
          extra_annotations=[
              rendering_parts.comment_color(
                  rendering_parts.text(f"  # value: {repr(item_value)}")
              )
          ],
      ),
      path,
  )

