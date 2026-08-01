
def _get_systemwide_numa_node_indices() -> set[int]:
    with open("/sys/devices/system/node/possible") as f:
        possible_nodes_str = f.read()

    return _get_set_of_int_from_ranges_str(possible_nodes_str)

