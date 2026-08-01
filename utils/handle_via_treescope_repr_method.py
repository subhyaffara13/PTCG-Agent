
def handle_via_treescope_repr_method(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    *,
    method_name: str = "__treescope_repr__",
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a type by calling its ``__treescope_repr__`` method, if it exists.

  The ``__treescope_repr__`` method can be used to add treescope support to
  custom classes. The method is expected to return a rendering in treescope's
  internal intermediate representation.

  The exact structure of the intermediate representation is an
  implementation detail and may change in future releases. Users should instead
  build a rendering using the high-level helpers in `treescope.repr_lib`, or
  the lower-level definitions in `treescope.rendering_parts`.

  Args:
    node: The node to render.
    path: An optional path to this node from the root.
    subtree_renderer: The renderer for subtrees of this node.
    method_name: Optional override for the name of the method to call. This is
      primarily intended for compatibility with treescope's original
      implementation as part of Penzai, which used __penzai_repr__.

  Returns:
    A rendering of this node, if it implements the __treescope_repr__ extension
    method.
  """
  treescope_repr_method = object_inspection.safely_get_real_method(
      node, method_name
  )
  if treescope_repr_method:
    return treescope_repr_method(path, subtree_renderer)
  else:
    return NotImplemented

