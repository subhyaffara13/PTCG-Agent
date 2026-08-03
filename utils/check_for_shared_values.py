from typing import Any

def check_for_shared_values(
    node: Any,
    path: str | None,
    node_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  # pylint: disable=g-doc-args,g-doc-return-or-yield
  """Wrapper hook to check for and annotate shared values.

  This wrapper should only be used by renderers that also include
  `build_styles_for_shared_values` in their HTML configuration and
  `setup_shared_value_context` in their context builders.

  Args:
    node: The node that has been rendered
    path: Optionally, a path to this node as a string.
    node_renderer: The inner renderer for this node. This should be used to
      render `node` itself into HTML tags.

  Returns:
    A possibly-modified representation of this object.

  Raises:
    RuntimeError: If called outside of the context constructed via
      setup_shared_value_context.
  """
  # pylint: enable=g-doc-args,g-doc-return-or-yield
  shared_object_tracker = _shared_object_ids_seen.get()
  if shared_object_tracker is None:
    raise RuntimeError(
        "`check_for_shared_values` should only be called in a shared value"
        " context! Make sure the current treescope renderer has"
        " `setup_shared_value_context` in its `context_builders`."
    )

  # Use object identity to track shared references and loops.
  node_id = id(node)

  # For types that we know are immutable, it's not necessary to render shared
  # references in a special way.
  safe_to_share = _is_safe_to_share(node)

  # Render the node normally.
  rendering = node_renderer(node, path)

  if not safe_to_share:
    # Mark this as possibly shared.
    if node_id in shared_object_tracker.seen_at_least_once:
      shared_object_tracker.seen_more_than_once.add(node_id)
    else:
      shared_object_tracker.seen_at_least_once[node_id] = node

    # Wrap it in a shared value wrapper; this will check to see if the same
    # node was seen more than once, and add an annotation if so.
    return rendering_parts.RenderableAndLineAnnotations(
        renderable=WithDynamicSharedPip(
            rendering.renderable,
            node_id=node_id,
            seen_more_than_once=shared_object_tracker.seen_more_than_once,
        ),
        annotations=rendering_parts.siblings(
            DynamicSharedCheck(
                if_shared=SharedWarningLabel(
                    rendering_parts.text(
                        f" # Repeated python obj at 0x{node_id:x}"
                    )
                ),
                node_id=node_id,
                seen_more_than_once=shared_object_tracker.seen_more_than_once,
            ),
            rendering.annotations,
        ),
    )

  return rendering

