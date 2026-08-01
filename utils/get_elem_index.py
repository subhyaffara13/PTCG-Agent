
def get_elem_index(elem_name, elem_list):
    """
    Helper function to return index of an item in a node list
    """
    elem_idx = -1
    for i in range(len(elem_list)):
        if elem_list[i] == elem_name:
            elem_idx = i
    return elem_idx

