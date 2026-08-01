
def _swap_node_partition(cut, node):
    return cut - {node} if node in cut else cut.union({node})

