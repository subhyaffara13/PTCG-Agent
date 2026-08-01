
def compare_cells(
    actual_cells,
    expected_cells,
    raise_on_first_difference=True,
    compare_outputs=True,
    compare_ids=True,
    cell_metadata_filter=None,
    allow_missing_code_cell_metadata=False,
    allow_missing_markdown_cell_metadata=False,
    allow_filtered_cell_metadata=False,
    allow_removed_final_blank_line=False,
):
    """Compare two collection of notebook cells"""
    test_cell_iter = iter(actual_cells)
    modified_cells = set()
    modified_cell_metadata = set()

    for i, ref_cell in enumerate(expected_cells, 1):
        try:
            test_cell = next(test_cell_iter)
        except StopIteration:
            if raise_on_first_difference:
                raise NotebookDifference(f"No cell corresponding to {ref_cell.cell_type} cell #{i}:\n{ref_cell.source}")
            modified_cells.update(range(i, len(expected_cells) + 1))
            break

        ref_lines = [line for line in ref_cell.source.splitlines() if not _BLANK_LINE.match(line)]
        test_lines = []

        # 1. test cell type
        if ref_cell.cell_type != test_cell.cell_type:
            if raise_on_first_difference:
                raise NotebookDifference(
                    f"When comparing cell #{i}: "
                    f"expecting a {ref_cell.cell_type} cell, but got a {test_cell.cell_type} cell.\n"
                    f"Expected content:\n{ref_cell.source}\nActual content:\n{test_cell.source}"
                )
            modified_cells.add(i)

        # Compare cell ids (introduced in nbformat 5.1.0)
        if compare_ids and test_cell.get("id") != ref_cell.get("id"):
            if raise_on_first_difference:
                raise NotebookDifference(
                    f"Cell ids differ on {test_cell['cell_type']} cell #{i}: '{test_cell.get('id')}' != '{ref_cell.get('id')}'"
                )
            modified_cells.add(i)

        # 2. test cell metadata
        if (ref_cell.cell_type == "code" and not allow_missing_code_cell_metadata) or (
            ref_cell.cell_type != "code" and not allow_missing_markdown_cell_metadata
        ):
            ref_metadata = ref_cell.metadata
            test_metadata = test_cell.metadata
            if allow_filtered_cell_metadata:
                ref_metadata = {key: ref_metadata[key] for key in ref_metadata if key not in _IGNORE_CELL_METADATA}
                test_metadata = {key: test_metadata[key] for key in test_metadata if key not in _IGNORE_CELL_METADATA}

            if ref_metadata != test_metadata:
                if raise_on_first_difference:
                    try:
                        compare(test_metadata, ref_metadata)
                    except AssertionError as error:
                        raise NotebookDifference(
                            "Metadata differ on {} cell #{}: {}\nCell content:\n{}".format(
                                test_cell.cell_type, i, str(error), ref_cell.source
                            )
                        )
                else:
                    modified_cell_metadata.update(set(test_metadata).difference(ref_metadata))
                    modified_cell_metadata.update(set(ref_metadata).difference(test_metadata))
                    for key in set(ref_metadata).intersection(test_metadata):
                        if ref_metadata[key] != test_metadata[key]:
                            modified_cell_metadata.add(key)

        test_lines.extend([line for line in test_cell.source.splitlines() if not _BLANK_LINE.match(line)])

        # 3. test cell content
        if ref_lines != test_lines:
            if raise_on_first_difference:
                try:
                    compare("\n".join(test_lines), "\n".join(ref_lines))
                except AssertionError as error:
                    raise NotebookDifference(f"Cell content differ on {test_cell.cell_type} cell #{i}: {str(error)}")
            else:
                modified_cells.add(i)

        # 3. bis test entire cell content
        if not same_content(ref_cell.source, test_cell.source, allow_removed_final_blank_line):
            if ref_cell.source != test_cell.source:
                if raise_on_first_difference:
                    diff = compare(test_cell.source, ref_cell.source, return_diff=True)
                    raise NotebookDifference(f"Cell content differ on {test_cell.cell_type} cell #{i}: {diff}")
                modified_cells.add(i)

        if not compare_outputs:
            continue

        if ref_cell.cell_type != "code":
            continue

        ref_cell = filtered_cell(
            ref_cell,
            preserve_outputs=compare_outputs,
            cell_metadata_filter=cell_metadata_filter,
        )
        test_cell = filtered_cell(
            test_cell,
            preserve_outputs=compare_outputs,
            cell_metadata_filter=cell_metadata_filter,
        )

        try:
            compare(test_cell, ref_cell)
        except AssertionError as error:
            if raise_on_first_difference:
                raise NotebookDifference(
                    "Cell outputs differ on {} cell #{}: {}".format(test_cell["cell_type"], i, str(error))
                )
            modified_cells.add(i)

    # More cells in the actual notebook?
    remaining_cell_count = 0
    while True:
        try:
            test_cell = next(test_cell_iter)
            if raise_on_first_difference:
                raise NotebookDifference(f"Additional {test_cell.cell_type} cell: {test_cell.source}")
            remaining_cell_count += 1
        except StopIteration:
            break

    if remaining_cell_count and not raise_on_first_difference:
        modified_cells.update(
            range(
                len(expected_cells) + 1,
                len(expected_cells) + 1 + remaining_cell_count,
            )
        )

    return modified_cells, modified_cell_metadata

