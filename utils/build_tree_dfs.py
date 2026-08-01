
def build_tree_dfs(
    world_state: openspiel_api.WorldState,
    all_infostates_map: List[Dict[str, InfoState]]
) -> Tuple[HistoryTreeNode, List[InfoState]]:
  """Builds the game tree by DFS traversal.

  Args:
    world_state: An openspiel game world state representation that will be the
      root of game tree.
    all_infostates_map: List of dictionaries (mapping from information state
      string representation to information state object) for each players
      (including chance player). This list will be empty when this function is
      called and it'll be population during DFS tree traversal.

  Returns:
    tree_node: Root of the game tree built in DFS traversal.
    infostate_nodes: List of information state (root) tree node for each player
    (including chance player).
  """
  tree_node = HistoryTreeNode(world_state)

  infostate_nodes = [
      InfoState(world_state, 1, world_state.get_infostate_string(1)),
      InfoState(world_state, 1, world_state.get_infostate_string(1)),
      InfoState(world_state, 2, world_state.get_infostate_string(2))
  ]
  for p in [cfr.Players.PLAYER_1, cfr.Players.PLAYER_2]:
    infostate_string = world_state.get_infostate_string(p)
    if infostate_string not in all_infostates_map[p]:
      all_infostates_map[p][infostate_string] = InfoState(
          world_state, p, infostate_string)

    infostate = all_infostates_map[p][infostate_string]
    infostate.add_history_node(tree_node)

    infostate_nodes[p] = infostate
  actions = world_state.get_actions()
  actions_chance, actions_p1, actions_p2 = actions

  for action_chance in actions_chance:
    for action_p1 in actions_p1:
      for action_p2 in actions_p2:
        child_state = copy.deepcopy(world_state)
        child_state.apply_actions((action_chance, action_p1, action_p2))
        child_tree_node, child_infostates = build_tree_dfs(
            child_state, all_infostates_map)

        tree_node.add_child(child_tree_node,
                            (action_chance, action_p1, action_p2))
        infostate_nodes[1].add_child_infostate(action_p1, child_infostates[1])
        infostate_nodes[2].add_child_infostate(action_p2, child_infostates[2])

  return tree_node, infostate_nodes

