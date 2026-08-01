
def filtered_cell(cell, preserve_outputs, cell_metadata_filter):
    """Cell type, metadata and source from given cell"""
    filtered = {
        "cell_type": cell.cell_type,
        "source": cell.source,
        "metadata": filter_metadata(cell.metadata, cell_metadata_filter, _IGNORE_CELL_METADATA),
    }

    if preserve_outputs:
        for key in ["execution_count", "outputs"]:
            if key in cell:
                filtered[key] = cell[key]

    return filtered

