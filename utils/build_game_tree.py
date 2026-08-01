
def build_game_tree(world_state: openspiel_api.WorldState) -> GameTree:
  """Builds game tree for CFR-based algorithms.

  Args:
    world_state: An openspiel game world state representation that will be the
      root of game tree.

  Returns:
    Calls GameTree function which returns the following:
    tree_node: Root of the game tree built in DFS traversal.
    infostate_nodes: List of information state (root) tree node for each player
    (including chance player).
  """
  all_infostates_map = [{}, {}, {}]
  first_history_node, infostate_nodes = build_tree_dfs(world_state,
                                                       all_infostates_map)
  return GameTree(first_history_node, infostate_nodes, all_infostates_map)

