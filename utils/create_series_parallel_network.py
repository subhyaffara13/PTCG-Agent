
def create_series_parallel_network(num_network_in_series,
                                   time_step_length=1,
                                   capacity=1):
  i = 0
  origin = "A_0->B_0"
  graph_dict = {}
  while i < num_network_in_series:
    tt_up = random.random() + time_step_length
    tt_down = random.random() + time_step_length
    graph_dict.update({
        f"A_{i}": {
            "connection": {
                f"B_{i}": {
                    "a": 0,
                    "b": 1.0,
                    "capacity": capacity,
                    "free_flow_travel_time": time_step_length
                }
            },
            "location": [0 + 3 * i, 0]
        },
        f"B_{i}": {
            "connection": {
                f"C_{i}": {
                    "a": 1.0,
                    "b": 1.0,
                    "capacity": capacity,
                    "free_flow_travel_time": tt_up
                },
                f"D_{i}": {
                    "a": 1.0,
                    "b": 1.0,
                    "capacity": capacity,
                    "free_flow_travel_time": tt_down
                }
            },
            "location": [1 + 3 * i, 0]
        },
        f"C_{i}": {
            "connection": {
                f"A_{i+1}": {
                    "a": 0,
                    "b": 1.0,
                    "capacity": capacity,
                    "free_flow_travel_time": time_step_length
                }
            },
            "location": [2 + 3 * i, 1]
        },
        f"D_{i}": {
            "connection": {
                f"A_{i+1}": {
                    "a": 0,
                    "b": 1.0,
                    "capacity": capacity,
                    "free_flow_travel_time": time_step_length
                }
            },
            "location": [2 + 3 * i, -1]
        }
    })
    i += 1
  graph_dict[f"A_{i}"] = {
      "connection": {
          "END": {
              "a": 0,
              "b": 1.0,
              "capacity": capacity,
              "free_flow_travel_time": time_step_length
          }
      },
      "location": [0 + 3 * i, 0]
  }
  graph_dict["END"] = {"connection": {}, "location": [1 + 3 * i, 0]}
  time_horizon = int(3.0 * (num_network_in_series + 1) / time_step_length)
  destination = f"A_{i}->END"
  adjacency_list = {
      key: list(value["connection"].keys())
      for key, value in graph_dict.items()
  }
  bpr_a_coefficient = {}
  bpr_b_coefficient = {}
  capacity = {}
  free_flow_travel_time = {}
  for o_node, value_dict in graph_dict.items():
    for d_node, section_dict in value_dict["connection"].items():
      road_section = dynamic_routing_utils._road_section_from_nodes(
          origin=o_node, destination=d_node)
      bpr_a_coefficient[road_section] = section_dict["a"]
      bpr_b_coefficient[road_section] = section_dict["b"]
      capacity[road_section] = section_dict["capacity"]
      free_flow_travel_time[road_section] = section_dict[
          "free_flow_travel_time"]
  node_position = {key: value["location"] for key, value in graph_dict.items()}
  return dynamic_routing_utils.Network(
      adjacency_list,
      node_position=node_position,
      bpr_a_coefficient=bpr_a_coefficient,
      bpr_b_coefficient=bpr_b_coefficient,
      capacity=capacity,
      free_flow_travel_time=free_flow_travel_time
  ), origin, destination, time_horizon

