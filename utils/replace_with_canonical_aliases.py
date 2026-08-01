
def replace_with_canonical_aliases(
    node: Any,
    path: str | None,
    node_renderer: renderers.TreescopeSubtreeRenderer,
    summarization_threshold: int = 20,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Rewrites objects to use well-known aliases when known.

  This rendering hook checks if the object is a well-known object exported by
  a public API, and if so, makes its short representation be its path in that
  API rather than its repr.

  Objects are looked up in canonical_aliases to determine if there is a
  specific alias registered for them. If not, but the object defines
  `__module__` and `__qualname__` attributes, these are used to determine the
  canonical alias instead.

  For objects whose fully-qualified name is longer than
  `summarization_threshold`, we shorten it when collapsed or not in roundtrip
  mode.

  Args:
    node: The node that has been rendered
    path: Optionally, a path to this node as a string.
    node_renderer: The inner renderer for this node. This should be used to
      render `node` itself into HTML tags.
    summarization_threshold: Threshold at which to omit the fully-qualified name
      except in roundtrip mode.

  Returns:
    A possibly-modified representation of this object, or NotImplemented.
  """
  maybe_alias = canonical_aliases.lookup_alias(
      node, infer_from_attributes=True, allow_relative=True
  )
  if not maybe_alias:
    # No alias.
    return NotImplemented

  qualified_name = str(maybe_alias)
  if "." not in qualified_name:
    name_rendering = qualified_name
  else:
    prefix, suffix = qualified_name.rsplit(".", 1)
    if len(qualified_name) > summarization_threshold:
      name_rendering = rendering_parts.siblings(
          rendering_parts.summarizable_condition(
              detail=rendering_parts.qualified_type_name_style(
                  rendering_parts.text(prefix + ".")
              )
          ),
          suffix,
      )
    else:
      name_rendering = rendering_parts.siblings(
          rendering_parts.qualified_type_name_style(
              rendering_parts.text(prefix + ".")
          ),
          suffix,
      )

  original_rendering = node_renderer(node, path=path)

  return rendering_parts.build_custom_foldable_tree_node(
      label=rendering_parts.comment_color_when_expanded(
          rendering_parts.siblings(
              rendering_parts.fold_condition(
                  expanded=rendering_parts.text("# ")
              ),
              name_rendering,
          )
      ),
      contents=rendering_parts.fold_condition(
          expanded=rendering_parts.indented_children([original_rendering])
      ),
      # Aliases should start collapsed regardless of layout.
      expand_state=rendering_parts.ExpandState.COLLAPSED,
      path=path,
  )

