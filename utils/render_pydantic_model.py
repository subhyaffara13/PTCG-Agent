
def render_pydantic_model(
    node: "pydantic.BaseModel",  # pytype: disable=attribute-error
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> rendering_parts.Rendering | type(NotImplemented):
  """Renders a pydantic model."""
  assert pydantic is not None, "pydantic is not available!"

  if pydantic.__version__.startswith("1."):
    fields = type(node).__fields__
  else:
    fields = type(node).model_fields
  return repr_lib.render_object_constructor(
      type(node),
      attributes={k: getattr(node, k) for k in fields.keys()},
      path=path,
      subtree_renderer=subtree_renderer,
      roundtrippable=True,
  )

