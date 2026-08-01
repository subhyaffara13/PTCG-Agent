
def digraph_edge_hamming_dist(g1, g2):
  """Returns number of directed edge mismatches between digraphs g1 and g2."""
  dist = 0
  for e1 in g1.edges:
    if e1 not in g2.edges:
      dist += 1
  return dist

