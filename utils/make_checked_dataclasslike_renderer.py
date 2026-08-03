from typing import Any

def make_checked_dataclasslike_renderer(
    cls: type[Any],
    fields: Sequence[str],
    fields_with_none_default: Sequence[str] = (),
) -> renderers.TreescopeNodeHandler:
  """Builds a roundtrippable renderer for a dataclass-like class.

  This function can be used to safely render classes that behave like Python
  dataclasses (i.e. they can be roundtripped by calling the constructor with
  attributes as keyword arguments). It is robust to potential new attributes
  being added by checking that it is possible to rebuild the instance correctly.
  This can be ued to render JAX builtin classes.

  Args:
    cls: The class to render.
    fields: A sequence of attribute names to render as keyword args.
    fields_with_none_default: A sequence of attribute names to render as keyword
      args only if they exist and their value is not None.

  Returns:
    A node handler for nodes of this type, which returns a simple rendering
    whenever the object is correctly described by these attributes.
  """

  def render_it(
      node: Any,
      path: str | None,
      subtree_renderer: renderers.TreescopeSubtreeRenderer,
  ) -> (
      rendering_parts.RenderableTreePart
      | rendering_parts.RenderableAndLineAnnotations
      | type(NotImplemented)
  ):
    if type(node) is not cls:  # pylint: disable=unidiomatic-typecheck
      return NotImplemented
    try:
      attributes = {k: getattr(node, k) for k in fields}
    except AttributeError:
      return NotImplemented
    for k in fields_with_none_default:
      if hasattr(node, k) and getattr(node, k) is not None:
        attributes[k] = getattr(node, k)

    # Make sure we can correctly round-trip it.
    rebuilt = cls(**attributes)
    if rebuilt != node:
      return NotImplemented
    else:
      return repr_lib.render_object_constructor(
          object_type=cls,
          attributes=attributes,
          path=path,
          subtree_renderer=subtree_renderer,
          roundtrippable=True,
      )

  return render_it

