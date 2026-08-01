
def handle_via_global_registry(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a type by looking it up in the global handler registry.

  If it is not feasible to define ``__treescope_repr__`` for a type, it can
  instead be registered in the global handler registry. This is a dictionary
  mapping types to functions that render a node of that type.

  The exact structure of the intermediate representation is an
  implementation detail and may change in future releases. Users should instead
  build a rendering using the high-level helpers in `treescope.repr_lib`, or
  the lower-level definitions in `treescope.rendering_parts`.

  Args:
    node: The node to render.
    path: An optional path to this node from the root.
    subtree_renderer: The renderer for subtrees of this node.

  Returns:
    A rendering of this node, if it was found in the global registry.
  """
  maybe_handler = type_registries.lookup_treescope_handler_for_type(type(node))
  if maybe_handler:
    return maybe_handler(node, path, subtree_renderer)
  else:
    return NotImplemented

