
def render_sequence_or_set(
    sequence: dict[Any, Any],
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> rendering_parts.RenderableAndLineAnnotations:
  """Renders a sequence or set to a foldable."""
  if (
      isinstance(sequence, tuple)
      and type(sequence) is not tuple  # pylint: disable=unidiomatic-typecheck
      and hasattr(type(sequence), "_fields")
  ):
    # This is actually a namedtuple, which renders with keyword arguments.
    return render_namedtuple_or_ast(sequence, path, subtree_renderer)

  children = []
  for i, child in enumerate(sequence):
    child_path = None if path is None else f"{path}[{repr(i)}]"
    children.append(subtree_renderer(child, path=child_path))

  force_trailing_comma = False
  if isinstance(sequence, tuple):
    before = "("
    after = ")"
    if type(sequence) is not tuple:  # pylint: disable=unidiomatic-typecheck
      # Subclass of `tuple`.
      assert not hasattr(type(sequence), "_fields"), "impossible: checked above"
      # Unusual situation: this is a subclass of `tuple`, but it isn't a
      # namedtuple. Assume we can call it with a single ordinary tuple as an
      # argument.
      before = rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(type(sequence)),
          "(" + before,
      )
      after = after + ")"
    force_trailing_comma = len(sequence) == 1
  elif isinstance(sequence, list):
    before = "["
    after = "]"
    if type(sequence) is not list:  # pylint: disable=unidiomatic-typecheck
      before = rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(type(sequence)),
          "(" + before,
      )
      after = after + ")"
  elif isinstance(sequence, set):
    if not sequence:
      before = "set("
      after = ")"
    else:  # pylint: disable=unidiomatic-typecheck
      before = "{"
      after = "}"

    if type(sequence) is not set:  # pylint: disable=unidiomatic-typecheck
      before = rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(type(sequence)),
          "(" + before,
      )
      after = after + ")"
  elif isinstance(sequence, frozenset):
    before = "frozenset({"
    after = "})"
    if type(sequence) is not frozenset:  # pylint: disable=unidiomatic-typecheck
      before = rendering_parts.siblings(
          rendering_parts.maybe_qualified_type_name(type(sequence)),
          "(" + before,
      )
      after = after + ")"
  else:
    raise ValueError(f"Unrecognized sequence {sequence}")

  if not children:
    return rendering_parts.build_one_line_tree_node(
        line=rendering_parts.siblings(before, after), path=path
    )
  else:
    return rendering_parts.build_foldable_tree_node_from_children(
        prefix=before,
        children=children,
        suffix=after,
        path=path,
        comma_separated=True,
        force_trailing_comma=force_trailing_comma,
        child_type_single_and_plural=("element", "elements"),
    )

