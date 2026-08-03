from typing import Any

def render_list_wrapper(
    object_type: type[Any],
    wrapped_sequence: Sequence[Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
    roundtrippable: bool = False,
    color: str | None = None,
) -> rendering_parts.Rendering:
  """Renders an object in "wrapped list format".

  This produces a rendering like `Foo([1, 2, 3])`, where Foo identifies the
  type of the object, and [1, 2, 3] is the list that Foo acts like. It is a
  *requirement* that these are accessible through `__getitem__`, e.g. as
  `obj[0]` or similar; otherwise, the path renderings will break.

  This can be used from within a `__treescope_repr__` implementation via ::

    def __treescope_repr__(self, path, subtree_renderer):
      return repr_lib.render_list_wrapper(
          object_type=type(self),
          wrapped_sequence=<sequence of items here>,
          path=path,
          subtree_renderer=subtree_renderer,
      )

  Args:
    object_type: The type of the object.
    wrapped_sequence: The sequence that the object wraps.
    path: The path to the object. When `render_list_wrapper` is called from
      `__treescope_repr__`, this should come from the `path` argument to
      `__treescope_repr__`.
    subtree_renderer: The renderer to use to render subtrees. When
      `render_list_wrapper` is called from `__treescope_repr__`, this should
      come from the `subtree_renderer` argument to `__treescope_repr__`.
    roundtrippable: Whether evaluating the rendering as Python code will produce
      an object that is equal to the original object. This implies that the
      constructor for `object_type` takes a single argument, which is a
      sequence, and that `object_type` then acts like that sequence.
    color: The background color to use for the object rendering. If None, does
      not use a background color. A utility for assigning a random color based
      on a string key is given in `treescope.formatting_util`.

  Returns:
    A rendering of the object, suitable for returning from `__treescope_repr__`.
  """
  if roundtrippable:
    constructor = rendering_parts.siblings(
        rendering_parts.maybe_qualified_type_name(object_type), "(["
    )
    closing_suffix = rendering_parts.text("])")
  else:
    constructor = rendering_parts.siblings(
        rendering_parts.roundtrip_condition(
            roundtrip=rendering_parts.text("<")
        ),
        rendering_parts.maybe_qualified_type_name(object_type),
        "([",
    )
    closing_suffix = rendering_parts.siblings(
        "])",
        rendering_parts.roundtrip_condition(
            roundtrip=rendering_parts.text(">")
        ),
    )

  children = []
  for i, child in enumerate(wrapped_sequence):
    child_path = None if path is None else f"{path}[{repr(i)}]"
    children.append(subtree_renderer(child, path=child_path))

  if not children:
    return rendering_parts.build_one_line_tree_node(
        line=rendering_parts.siblings(constructor, closing_suffix), path=path
    )
  else:
    return rendering_parts.build_foldable_tree_node_from_children(
        prefix=constructor,
        children=children,
        suffix=closing_suffix,
        path=path,
        comma_separated=True,
        force_trailing_comma=False,
        background_color=color,
        child_type_single_and_plural=("element", "elements"),
    )

