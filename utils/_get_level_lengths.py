
def _get_level_lengths(
    index: Index,
    sparsify: bool,
    max_index: int,
    hidden_elements: Sequence[int] | None = None,
):
    """
    Given an index, find the level length for each element.

    Parameters
    ----------
    index : Index
        Index or columns to determine lengths of each element
    sparsify : bool
        Whether to hide or show each distinct element in a MultiIndex
    max_index : int
        The maximum number of elements to analyse along the index due to trimming
    hidden_elements : sequence of int
        Index positions of elements hidden from display in the index affecting
        length

    Returns
    -------
    Dict :
        Result is a dictionary of (level, initial_position): span
    """
    if isinstance(index, MultiIndex):
        levels = index._format_multi(sparsify=lib.no_default, include_names=False)
    else:
        levels = index._format_flat(include_name=False)

    if hidden_elements is None:
        hidden_elements = []

    lengths = {}
    if not isinstance(index, MultiIndex):
        for i, value in enumerate(levels):
            if i not in hidden_elements:
                lengths[(0, i)] = 1
        return lengths

    for i, lvl in enumerate(levels):
        visible_row_count = 0  # used to break loop due to display trimming
        for j, row in enumerate(lvl):
            if visible_row_count > max_index:
                break
            if not sparsify:
                # then lengths will always equal 1 since no aggregation.
                if j not in hidden_elements:
                    lengths[(i, j)] = 1
                    visible_row_count += 1
            elif (row is not lib.no_default) and (j not in hidden_elements):
                # this element has not been sparsified so must be the start of section
                last_label = j
                lengths[(i, last_label)] = 1
                visible_row_count += 1
            elif row is not lib.no_default:
                # even if the above is hidden, keep track of it in case length > 1 and
                # later elements are visible
                last_label = j
                lengths[(i, last_label)] = 0
            elif j not in hidden_elements:
                # then element must be part of sparsified section and is visible
                visible_row_count += 1
                if visible_row_count > max_index:
                    break  # do not add a length since the render trim limit reached
                if lengths[(i, last_label)] == 0:
                    # if previous iteration was first-of-section but hidden then offset
                    last_label = j
                    lengths[(i, last_label)] = 1
                else:
                    # else add to previous iteration
                    lengths[(i, last_label)] += 1

    non_zero_lengths = {
        element: length for element, length in lengths.items() if length >= 1
    }

    return non_zero_lengths

