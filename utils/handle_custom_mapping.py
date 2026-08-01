
def handle_custom_mapping(
    node: Mapping[Any, Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    *,
    roundtrippable: bool = False,
) -> rendering_parts.Rendering:
  """Handler for custom mappings.

  This wraps the `render_dictionary_wrapper` function so that it can be easily
  used as a type registry entry for custom mappings from third-party libraries.
  It assumes that the node itself is a mapping.

  For instance, if you know that third-party library type ``SomeMapping`` is a
  mapping, you can register a handler for it like this::

    treescope.type_registries.TREESCOPE_HANDLER_REGISTRY[SomeMapping] = (
        treescope.repr_lib.handle_custom_mapping
    )

  Args:
    node: The node to render.
    path: The path to the node.
    subtree_renderer: The renderer to use to render subtrees.
    roundtrippable: Whether evaluating the rendering as Python code will produce
      an object that is equal to the original object. This implies that the
      constructor for ``type(node)`` takes a single argument, which is a
      dictionary, and that ``type(node)`` then acts like that dictionary.

  Returns:
    A rendering of the node.
  """
  try:
    converted_to_dict = dict(node)
  except Exception as e:
    raise TypeError(
        "Cannot use handle_custom_mapping to handle a non-mapping; you should"
        " only use handle_custom_mapping when you already know this object is a"
        " mapping (for instance, as an entry in"
        " `treescope.type_registries.TREESCOPE_HANDLER_REGISTRY` for a mapping"
        " type.)"
    ) from e
  return render_dictionary_wrapper(
      object_type=type(node),
      wrapped_dict=converted_to_dict,
      path=path,
      subtree_renderer=subtree_renderer,
      roundtrippable=roundtrippable,
  )

