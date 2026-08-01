
def render_ndarrays(
    node: np.ndarray,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a numpy array."""
  del subtree_renderer
  assert isinstance(node, np.ndarray)
  adapter = NumpyArrayAdapter()

  def _placeholder() -> rendering_parts.RenderableTreePart:
    return rendering_parts.deferred_placeholder_style(
        adapter.get_array_summary(node, fast=True)
    )

  def _thunk(placeholder_expand_state: rendering_parts.ExpandState | None):
    # Is this array simple enough to render without a summary?
    node_repr = repr(node)
    if "\n" not in node_repr and "..." not in node_repr:
      rendering = rendering_parts.text(f"np.{node_repr}")
    else:
      if node_repr.count("\n") <= 15:
        if placeholder_expand_state is None:
          default_expand_state = rendering_parts.ExpandState.WEAKLY_EXPANDED
        else:
          default_expand_state = placeholder_expand_state
      else:
        # Always start big NDArrays in collapsed mode to hide irrelevant detail.
        default_expand_state = rendering_parts.ExpandState.COLLAPSED

      # Render it with a summary.
      summarized = adapter.get_array_summary(node, fast=False)
      rendering = rendering_parts.build_custom_foldable_tree_node(
          label=rendering_parts.abbreviation_color(
              rendering_parts.comment_color_when_expanded(
                  rendering_parts.siblings(
                      rendering_parts.fold_condition(
                          expanded=rendering_parts.text("# "),
                          collapsed=rendering_parts.text("<"),
                      ),
                      summarized,
                      rendering_parts.fold_condition(
                          collapsed=rendering_parts.text(">")
                      ),
                  )
              )
          ),
          contents=rendering_parts.fold_condition(
              expanded=rendering_parts.indented_children(
                  [rendering_parts.text(node_repr)]
              )
          ),
          path=path,
          expand_state=default_expand_state,
      ).renderable

    return rendering

  return rendering_parts.RenderableAndLineAnnotations(
      renderable=lowering.maybe_defer_rendering(
          main_thunk=_thunk, placeholder_thunk=_placeholder
      ),
      annotations=rendering_parts.build_copy_button(path),
  )

