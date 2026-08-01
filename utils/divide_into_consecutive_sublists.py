
def divide_into_consecutive_sublists(indices: list[int]) -> list[list[int]]:
    n = len(indices)
    if n <= 1:
        return [indices]

    # Initialize the list of sublists
    sublists = []

    # Iterate over the indices
    i = 0
    while i < n:
        # Initialize the current sublist
        sublist = [indices[i]]

        # Iterate over the remaining indices
        j = i + 1
        while j < n and indices[j] == indices[j - 1] + 1:
            # Add the next index to the current sublist
            sublist.append(indices[j])
            j += 1

        # Add the current sublist to the list of sublists
        sublists.append(sublist)
        # Move to the next index
        i = j

    return sublists

