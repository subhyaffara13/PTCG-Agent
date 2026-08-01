
def is_equitable(G, coloring, num_colors=None):
    """Determines if the coloring is valid and equitable for the graph G."""

    if not is_coloring(G, coloring):
        return False

    # Verify whether it is equitable.
    color_set_size = defaultdict(int)
    for color in coloring.values():
        color_set_size[color] += 1

    if num_colors is not None:
        for color in range(num_colors):
            if color not in color_set_size:
                # These colors do not have any vertices attached to them.
                color_set_size[color] = 0

    # If there are more than 2 distinct values, the coloring cannot be equitable
    all_set_sizes = set(color_set_size.values())
    if len(all_set_sizes) == 0 and num_colors is None:  # Was an empty graph
        return True
    elif len(all_set_sizes) == 1:
        return True
    elif len(all_set_sizes) == 2:
        a, b = list(all_set_sizes)
        return abs(a - b) <= 1
    else:  # len(all_set_sizes) > 2:
        return False

