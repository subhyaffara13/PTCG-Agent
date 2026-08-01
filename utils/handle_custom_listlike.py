
def handle_custom_listlike(
    node: Sequence[Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    *,
    roundtrippable: bool = False,
) -> rendering_parts.Rendering:
  """Handler for custom list-like sequences.

  This wraps the `render_list_wrapper` function so that it can be easily
  used as a type registry entry for custom sequences from third-party libraries.
  It assumes that the node itself is a sequence.

  For instance, if you know that third-party library type ``SomeSequence`` is a
  sequence, you can register a handler for it like this::

    treescope.type_registries.TREESCOPE_HANDLER_REGISTRY[SomeSequence] = (
        treescope.repr_lib.handle_custom_listlike
    )

  Args:
    node: The node to render.
    path: The path to the node.
    subtree_renderer: The renderer to use to render subtrees.
    roundtrippable: Whether evaluating the rendering as Python code will produce
      an object that is equal to the original object. This implies that the
      constructor for ``type(node)`` takes a single argument, which is a
      sequence, and that ``type(node)`` then acts like that sequence.

  Returns:
    A rendering of the node.
  """
  try:
    converted_to_list = list(node)
  except Exception as e:
    raise TypeError(
        "Cannot use handle_custom_listlike to handle a non-sequence; you should"
        " only use handle_custom_listlike when you already know this object is"
        " a sequence (for instance, as an entry in"
        " `treescope.type_registries.TREESCOPE_HANDLER_REGISTRY` for a sequence"
        " type.)"
    ) from e
  return render_list_wrapper(
      object_type=type(node),
      wrapped_sequence=converted_to_list,
      path=path,
      subtree_renderer=subtree_renderer,
      roundtrippable=roundtrippable,
  )

