
def align_trace_from_beginning(
    entries: dict[int, list[dict[str, Any]]],
) -> dict[int, list[dict[str, Any]]]:
    """
    Align the trace entries by record ID for entries.
    This function takes a dictionary of rank names to lists of trace entries as input.
    Each trace entry is a dictionary containing information about a collective operation,
    including its unique identifier (`record_id` is monotonically increasing as we write into the ring buffer).
    The function finds the largest starting point across all ranks by taking the maximum
    `record_id` value of the first entry in each rank. Finally, it filters out any
    entries with `record_id` values less than the maximum starting point.
    The function returns the updated dictionary of sorted and filtered trace entries.

    Args:
        entries (Dict[str, List[Dict[str, Any]]]): A dictionary of rank names to lists of trace entries.

    Returns:
        entries (Dict[str, List[Dict[str, Any]]]): Entries sorted by record ID and filtered by the maximum starting point.
    """

    maximum_starting_record_id = 0
    for rank in entries:
        # Although this is a ring buffer, we already sort the entries by `record_id` when dumping, we just
        # need to find the largest starting point. For example, if the buffer has the following entries:
        # Rank 0: [0, 1, 2, 3, 4, 5, 6]
        # Rank 1: [1, 2, 3, 4, 5, 6, 7]
        # Rank 2: [2, 3, 4, 5, 6, 7, 8]
        # Rank 3: [0, 1, 2, 3, 4, 5, None]
        # Then we should start from collective 2 not 0 because any collective before,
        # we don't have complete records from all ranks so we need to ignore them.
        # If we don't have any trace from some ranks, ignore them
        # as well.
        if len(entries[rank]) == 0:
            continue
        first_record_id = entries[rank][0]["record_id"]
        maximum_starting_record_id = max(maximum_starting_record_id, first_record_id)

    for rank in entries:
        entries[rank] = [
            entry
            for entry in entries[rank]
            if entry["record_id"] >= maximum_starting_record_id
        ]

    return entries

