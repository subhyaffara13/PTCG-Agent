
def render_torch_modules(
    node: torch.nn.Module,
    path: str | None,
    subtree_renderer: renderers.TreescopeSubtreeRenderer,
) -> (
    rendering_parts.RenderableTreePart
    | rendering_parts.RenderableAndLineAnnotations
    | type(NotImplemented)
):
  """Renders a torch module."""
  assert torch is not None, "PyTorch is not available."
  assert isinstance(node, torch.nn.Module)
  node_type = type(node)
  constructor = rendering_parts.siblings(
      rendering_parts.roundtrip_condition(roundtrip=rendering_parts.text("<")),
      rendering_parts.maybe_qualified_type_name(node_type),
      "(",
  )
  closing_suffix = rendering_parts.siblings(
      ")",
      rendering_parts.roundtrip_condition(roundtrip=rendering_parts.text(">")),
  )

  if hasattr(node, "__treescope_color__") and callable(
      node.__treescope_color__
  ):
    background_color, background_pattern = (
        formatting_util.parse_simple_color_and_pattern_spec(
            node.__treescope_color__(), node_type.__name__
        )
    )
  elif type(node) is torch.nn.Sequential:  # pylint: disable=unidiomatic-typecheck
    background_color, background_pattern = (
        formatting_util.parse_simple_color_and_pattern_spec(
            ("#cdcdcd", "color-mix(in oklab, #cdcdcd 25%, white)")
        )
    )
  elif type(node).forward is torch.nn.Module.forward:
    # No implementation of forward. Don't color-code; this is probably a
    # container like ModuleList or ModuleDict.
    background_color = None
    background_pattern = None
  else:
    type_string = node_type.__module__ + "." + node_type.__qualname__
    background_color = formatting_util.color_from_string(type_string)
    background_pattern = None

  children = []
  prefers_expand = False
  attr_children = None
  has_attr_children_expander = False

  # Render constant attributes.
  if show_dynamic_attributes.get():
    attr_children = []
    key_order = [
        key
        for key in vars(node)
        if not key.startswith("_") and key != "training"
    ]
    if "training" in vars(node):
      key_order.append("training")
    for attr in key_order:
      value = vars(node)[attr]
      child_path = None if path is None else f"{path}.{attr}"
      attr_children.append(
          rendering_parts.build_full_line_with_annotations(
              rendering_parts.siblings_with_annotations(
                  f"{attr}=",
                  subtree_renderer(value, path=child_path),
                  ",",
                  rendering_parts.fold_condition(
                      collapsed=rendering_parts.text(" ")
                  ),
              )
          )
      )
    if len(attr_children) <= 1:
      children.extend(attr_children)
    else:
      has_attr_children_expander = True
      children.append(
          rendering_parts.build_custom_foldable_tree_node(
              label=rendering_parts.fold_condition(
                  expanded=rendering_parts.comment_color(
                      rendering_parts.text("# Attributes:")
                  ),
              ),
              contents=rendering_parts.on_separate_lines(attr_children),
              path=None,
              expand_state=rendering_parts.ExpandState.COLLAPSED,
          )
      )
  else:
    extra_repr = node.extra_repr()
    if extra_repr:
      if not extra_repr.strip().endswith(","):
        extra_repr = extra_repr + ", "
      if "\n" in extra_repr:
        children.append(
            rendering_parts.on_separate_lines(extra_repr.split("\n"))
        )
        prefers_expand = True
      else:
        children.append(rendering_parts.text(extra_repr))

  # Render parameters and buffers
  for group_name, group in (
      ("Parameters", node.named_parameters(recurse=False)),
      ("Buffers", node.named_buffers(recurse=False)),
  ):
    group = list(group)
    if group:
      children.append(
          rendering_parts.fold_condition(
              expanded=rendering_parts.comment_color(
                  rendering_parts.text(f"# {group_name}:")
              )
          )
      )
      for name, value in group:
        child_path = None if path is None else f"{path}.{name}"
        children.append(
            rendering_parts.build_full_line_with_annotations(
                rendering_parts.siblings_with_annotations(
                    f"{name}=",
                    subtree_renderer(value, path=child_path),
                    ",",
                    rendering_parts.fold_condition(
                        collapsed=rendering_parts.text(" ")
                    ),
                )
            )
        )

  # Render submodules.
  submodules = list(node.named_children())
  if submodules:
    children.append(
        rendering_parts.fold_condition(
            expanded=rendering_parts.comment_color(
                rendering_parts.text("# Child modules:")
            )
        )
    )
    for name, submod in submodules:
      prefers_expand = True
      if name.isidentifier() and not keyword.iskeyword(name):
        child_path = None if path is None else f"{path}.{name}"
        keystr = f"{name}="
      else:
        child_path = f"{path}.get_submodule({repr(name)})"
        keystr = f"({name}): "
      children.append(
          rendering_parts.build_full_line_with_annotations(
              rendering_parts.siblings_with_annotations(
                  keystr,
                  subtree_renderer(submod, path=child_path),
                  ",",
                  rendering_parts.fold_condition(
                      collapsed=rendering_parts.text(" ")
                  ),
              )
          )
      )

  # If there are only dynamic attributes, don't add the level of indirection.
  if has_attr_children_expander and len(children) == 1:
    children = attr_children

  # Heuristic: If a module doesn't have any submodules, mark it collapsed, to
  # match the behavior of PyTorch repr.
  if prefers_expand:
    expand_state = rendering_parts.ExpandState.WEAKLY_EXPANDED
  else:
    expand_state = rendering_parts.ExpandState.COLLAPSED

  return rendering_parts.build_foldable_tree_node_from_children(
      prefix=constructor,
      children=children,
      suffix=closing_suffix,
      path=path,
      background_color=background_color,
      background_pattern=background_pattern,
      expand_state=expand_state,
      child_type_single_and_plural=("child", "children"),
  )

