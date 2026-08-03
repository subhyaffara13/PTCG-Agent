import os

def ranked_pairs_viz(model_names, dataset):
  """Produce the ranked pairs visualization."""

  alternatives = model_names[:]
  profile = base.PreferenceProfile(alternatives=alternatives)
  num_alternatives = len(alternatives)
  alt_dict = profile.alternatives_dict
  for datapoint in dataset:
    alt_a, alt_b, outcome = datapoint
    if outcome == 0:
      pass
    elif outcome == -1:
      profile.add_vote([alt_a, alt_b])
    elif outcome == 1:
      profile.add_vote([alt_b, alt_a])
  margin_matrix = profile.margin_matrix()
  method = ranked_pairs.RankedPairsVoting()
  outcome = method.run_election(profile)
  graph_mat = outcome.graph
  # Visualize only over the top 8:
  keep_alternatives = [
      "gpt-4",
      "claude-v1",
      "claude-instant-v1",
      "guanaco-33b",
      "gpt-3.5-turbo",
      "wizardlm-13b",
      "palm-2",
      "vicuna-13b",
  ]
  keep_alternatives.sort()
  for j in range(num_alternatives):
    idx = num_alternatives - j - 1
    alt = alternatives[idx]
    if alt not in keep_alternatives:
      graph_mat = np.delete(graph_mat, (idx), axis=0)
      graph_mat = np.delete(graph_mat, (idx), axis=1)
  orig_alternatives = model_names[:]
  alternatives = keep_alternatives
  m = len(alternatives)
  graph = pgv.AGraph(directed=True, strict=True)
  for alternative in alternatives:
    graph.add_node(alternative)
  for i in range(m):
    for j in range(m):
      if graph_mat[i, j] == 1:
        graph.add_edge(alternatives[i], alternatives[j])
        idx_i = alt_dict[alternatives[i]]
        idx_j = alt_dict[alternatives[j]]
        edge = graph.get_edge(
            orig_alternatives[idx_i], orig_alternatives[idx_j]
        )
        edge.attr["label"] = margin_matrix[idx_i, idx_j]
  dot_path = os.path.join(tempfile.gettempdir(), "chatbot_arena_rps.dot")
  png_path = os.path.join(tempfile.gettempdir(), "chatbot_arena_rps.png")
  graph.write(dot_path)  # write to simple.dot
  graph.draw(
      png_path,
      # args='-Gdpi=100',
      prog="dot",
  )  # , args="-n2")  # draw
  print(f"Wrote to {png_path}")

