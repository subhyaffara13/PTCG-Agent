
def default_edge_decorator(parent, unused_child, action):
  """Decorates a state-node of the game tree.

  This method can be called by a custom decorator to prepopulate the attributes
  dictionary. Then only relevant attributes need to be changed, or added.

  Args:
    parent: The parent state.
    unused_child: The child state, not used in the default decorator.
    action: `int` the selected action in the parent state.

  Returns:
    `dict` with graphviz node style attributes.
  """
  player = parent.current_player()
  attrs = {
      "label": " " + parent.action_to_string(player, action),
      "fontsize": _FONTSIZE,
      "arrowsize": _ARROWSIZE
  }
  attrs["color"] = _PLAYER_COLORS.get(player, "black")
  return attrs

