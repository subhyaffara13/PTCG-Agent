
def render_precision(
    node: jax.lax.Precision,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders jax.lax.Precision."""
  assert jax is not None, "JAX is not available."
  if type(node) is not jax.lax.Precision:  # pylint: disable=unidiomatic-typecheck
    return NotImplemented
  return repr_lib.render_enumlike_item(
      object_type=jax.lax.Precision,
      item_name=node.name,
      item_value=node.value,
      path=path,
      subtree_renderer=subtree_renderer,
  )

