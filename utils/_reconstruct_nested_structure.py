
def _reconstruct_nested_structure(indices, processed_images):
    """Helper function to reconstruct a single level nested structure."""
    # Get the number of sublists (handles empty sublists like in [[], [image]])
    num_sublists = indices.pop("_num_sublists", None)

    # Group indices by outer index
    nested_indices = defaultdict(list)
    for i, j in indices:
        nested_indices[i].append(j)

    # Determine the number of outer sublists
    if num_sublists is not None:
        max_outer_idx = num_sublists - 1
    elif nested_indices:
        max_outer_idx = max(nested_indices.keys())
    else:
        return []

    # Create the result structure
    result = []
    for i in range(max_outer_idx + 1):
        if i not in nested_indices:
            result.append([])
        else:
            inner_max_idx = max(nested_indices[i])
            inner_list = [None] * (inner_max_idx + 1)
            for j in nested_indices[i]:
                shape, idx = indices[(i, j)]
                inner_list[j] = processed_images[shape][idx]
            result.append(inner_list)

    return result

