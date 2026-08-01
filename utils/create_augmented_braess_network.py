
def create_augmented_braess_network(capacity):
  graph_dict = {
      "A": {
          "connection": {
              "B": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 0
              }
          },
          "location": [0, 0]
      },
      "B": {
          "connection": {
              "C": {
                  "a": 1.0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 1.0
              },
              "D": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 2.0
              }
          },
          "location": [1, 0]
      },
      "C": {
          "connection": {
              "D": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 0.25
              },
              "E": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 2.0
              }
          },
          "location": [2, 1]
      },
      "D": {
          "connection": {
              "E": {
                  "a": 1,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 1.0
              },
              "G": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 0.0
              }
          },
          "location": [2, -1]
      },
      "E": {
          "connection": {
              "F": {
                  "a": 0,
                  "b": 1.0,
                  "capacity": capacity,
                  "free_flow_travel_time": 0.0
              }
          },
          "location": [3, 0]
      },
      "F": {
          "connection": {},
          "location": [4, 0]
      },
      "G": {
          "connection": {},
          "location": [3, -1]
      }
  }
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
      free_flow_travel_time=free_flow_travel_time)

