
def render_dtype_instances(
    node: Any,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a np.dtype, adding the `np.` qualifier."""
  del subtree_renderer
  if not isinstance(node, np.dtype):
    return NotImplemented

  dtype_name = node.name
  if dtype_name in np.sctypeDict and node is np.dtype(
      np.sctypeDict[dtype_name]
  ):
    # Use the named type. (Sometimes extended dtypes don't print in a
    # roundtrippable way otherwise.)
    dtype_string = f"dtype({repr(dtype_name)})"
  else:
    # Hope that `repr` is already round-trippable (true for builtin numpy types)
    # and add the "numpy." prefix as needed.
    dtype_string = repr(node)

  return rendering_parts.build_one_line_tree_node(
      line=rendering_parts.siblings(
          rendering_parts.roundtrip_condition(
              roundtrip=rendering_parts.text("np.")
          ),
          dtype_string,
      ),
      path=path,
  )

