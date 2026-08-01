
def default_node_decorator(state):
  """Decorates a state-node of the game tree.

  This method can be called by a custom decorator to prepopulate the attributes
  dictionary. Then only relevant attributes need to be changed, or added.

  Args:
    state: The state.

  Returns:
    `dict` with graphviz node style attributes.
  """
  player = state.current_player()
  attrs = {
      "label": "",
      "fontsize": _FONTSIZE,
      "width": _WIDTH,
      "height": _HEIGHT,
      "margin": _MARGIN
  }
  if state.is_terminal():
    attrs["label"] = ", ".join(map(str, state.returns()))
    attrs["shape"] = "diamond"
  elif state.is_chance_node():
    attrs["shape"] = "point"
    attrs["width"] = _WIDTH / 2.
    attrs["height"] = _HEIGHT / 2.
  else:
    attrs["label"] = str(state.information_state_string())
    attrs["shape"] = _PLAYER_SHAPES.get(player, "ellipse")
    attrs["color"] = _PLAYER_COLORS.get(player, "black")
  return attrs

