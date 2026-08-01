
def render_dictionary_wrapper(
    object_type: type[Any],
    wrapped_dict: Mapping[str, Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    roundtrippable: bool = False,
    color: str | None = None,
) -> rendering_parts.Rendering:
  """Renders an object in "wrapped dictionary format".

  This produces a rendering like `Foo({"bar": 1, "baz": 2})`, where Foo
  identifies the type of the object, and "bar" and "baz" are the keys in the
  dictionary that Foo acts like. It is a *requirement* that these are accessible
  through `__getitem__`, e.g. as `obj["bar"]` or similar; otherwise, the path
  renderings will break.

  This can be used from within a `__treescope_repr__` implementation via ::

    def __treescope_repr__(self, path, subtree_renderer):
      return repr_lib.render_dictionary_wrapper(
          object_type=type(self),
          wrapped_dict=<dict of items here>,
          path=path,
          subtree_renderer=subtree_renderer,
      )

  Args:
    object_type: The type of the object.
    wrapped_dict: The dictionary that the object wraps.
    path: The path to the object. When `render_object_constructor` is called
      from `__treescope_repr__`, this should come from the `path` argument to
      `__treescope_repr__`.
    subtree_renderer: The renderer to use to render subtrees. When
      `render_object_constructor` is called from `__treescope_repr__`, this
      should come from the `subtree_renderer` argument to `__treescope_repr__`.
    roundtrippable: Whether evaluating the rendering as Python code will produce
      an object that is equal to the original object. This implies that the
      constructor for `object_type` takes a single argument, which is a
      dictionary, and that `object_type` then acts like that dictionary.
    color: The background color to use for the object rendering. If None, does
      not use a background color. A utility for assigning a random color based
      on a string key is given in `treescope.formatting_util`. (By convention,
      wrapped dictionaries aren't usually assigned a color in Treescope.)

  Returns:
    A rendering of the object, suitable for returning from `__treescope_repr__`.
  """
  if roundtrippable:
    constructor = rendering_parts.siblings(
        rendering_parts.maybe_qualified_type_name(object_type), "({"
    )
    closing_suffix = rendering_parts.text("})")
  else:
    constructor = rendering_parts.siblings(
        rendering_parts.roundtrip_condition(
            roundtrip=rendering_parts.text("<")
        ),
        rendering_parts.maybe_qualified_type_name(object_type),
        "({",
    )
    closing_suffix = rendering_parts.siblings(
        "})",
        rendering_parts.roundtrip_condition(
            roundtrip=rendering_parts.text(">")
        ),
    )

  children = []
  for i, (key, value) in enumerate(wrapped_dict.items()):
    child_path = None if path is None else f"{path}[{repr(key)}]"

    if i < len(wrapped_dict) - 1:
      # Not the last child. Always show a comma, and add a space when
      # collapsed.
      comma_after = rendering_parts.siblings(
          ",",
          rendering_parts.fold_condition(collapsed=rendering_parts.text(" ")),
      )
    else:
      # Last child: only show the comma when the node is expanded.
      comma_after = rendering_parts.fold_condition(
          expanded=rendering_parts.text(",")
      )

    key_rendering = subtree_renderer(key)
    value_rendering = subtree_renderer(value, path=child_path)

    if (
        key_rendering.renderable.collapsed_width < 40
        and not key_rendering.renderable.foldables_in_this_part()
        and (
            key_rendering.annotations is None
            or key_rendering.annotations.collapsed_width == 0
        )
    ):
      # Simple enough to render on one line.
      children.append(
          rendering_parts.siblings_with_annotations(
              key_rendering, ": ", value_rendering, comma_after
          )
      )
    else:
      # Should render on multiple lines.
      children.append(
          rendering_parts.siblings(
              rendering_parts.build_full_line_with_annotations(
                  key_rendering,
                  ":",
                  rendering_parts.fold_condition(
                      collapsed=rendering_parts.text(" ")
                  ),
              ),
              rendering_parts.indented_children([
                  rendering_parts.siblings_with_annotations(
                      value_rendering, comma_after
                  ),
                  rendering_parts.fold_condition(
                      expanded=rendering_parts.vertical_space("0.5em")
                  ),
              ]),
          )
      )

  return rendering_parts.build_foldable_tree_node_from_children(
      prefix=constructor,
      children=children,
      suffix=closing_suffix,
      path=path,
      background_color=color,
      child_type_single_and_plural=("item", "items"),
  )

