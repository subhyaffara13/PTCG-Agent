import copy

def restore_filtered_metadata(filtered_metadata, unfiltered_metadata, user_filter, default_filter):
    """Update the filtered metadata with the part of the unfiltered one that matches the filter"""
    filtered_unfiltered_metadata = filter_metadata(unfiltered_metadata, user_filter, default_filter)

    metadata = copy(filtered_metadata)
    for key in unfiltered_metadata:
        if key not in filtered_unfiltered_metadata:
            # We don't want to restore the line_to_next_cell metadata from the ipynb file, see #761
            if key not in _JUPYTEXT_CELL_METADATA:
                metadata[key] = unfiltered_metadata[key]

    return metadata

