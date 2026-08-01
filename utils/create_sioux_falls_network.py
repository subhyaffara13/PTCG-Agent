
def create_sioux_falls_network():
  """Returns Sioux Falls network object (Network).

  Adds the origin and destination link to the adjacency list
  __SIOUX_FALLS_ADJACENCY, to the BPR coefficients
  __SIOUX_FALLS_FREE_FLOW_TRAVEL_TIME and __SIOUX_FALLS_BPR_A_COEFF and to the
  node positions __SIOUX_FALLS_NODES and returns the network.
  The BPR (Burean of Public Roads) coefficients are the coefficients used to
  compute the travel time as a function of the volume on each link.
  """
  adjacency = {}
  free_flow_travel_time = __SIOUX_FALLS_FREE_FLOW_TRAVEL_TIME.copy()
  bpr_a_coeff = __SIOUX_FALLS_BPR_A_COEFF.copy()
  node_position = {}

  for k, nodes in __SIOUX_FALLS_ADJACENCY.items():
    adjacency[k] = nodes + [f"aft_{k}"]
    adjacency[f"bef_{k}"] = [k]
    adjacency[f"aft_{k}"] = []
    free_flow_travel_time[f"bef_{k}->{k}"] = 0
    free_flow_travel_time[f"{k}->aft_{k}"] = 0
    bpr_a_coeff[f"bef_{k}->{k}"] = 0
    bpr_a_coeff[f"{k}->aft_{k}"] = 0

  for node, coord in __SIOUX_FALLS_NODES.items():
    node_position[node] = coord
    node_position[f"bef_{node}"] = coord
    node_position[f"aft_{node}"] = coord

  return dynamic_routing_utils.Network(
      adjacency,
      node_position=node_position,
      bpr_a_coefficient=bpr_a_coeff,
      bpr_b_coefficient={k: 4 for k in bpr_a_coeff},
      capacity={k: 1 for k in bpr_a_coeff},
      free_flow_travel_time=free_flow_travel_time)

