
def map_outputs_to_inputs(cells_inputs, cells_outputs):
    """Returns a map i->(j or None) that maps the cells with outputs to the input cells"""
    n_in = len(cells_inputs)
    n_out = len(cells_outputs)
    outputs_map = [None] * n_in

    # First rule: match based on cell type, content, in increasing order, for each cell type
    first_unmatched_output_per_cell_type = {}
    for i in range(n_in):
        cell_input = cells_inputs[i]
        for j in range(first_unmatched_output_per_cell_type.get(cell_input.cell_type, 0), n_out):
            cell_output = cells_outputs[j]
            if cell_input.cell_type == cell_output.cell_type and same_content(cell_input.source, cell_output.source):
                outputs_map[i] = j
                first_unmatched_output_per_cell_type[cell_input.cell_type] = j + 1
                break

    # Second rule: match unused outputs based on cell type and content
    # Third rule: is the new cell the final part of a previous cell with outputs?
    unused_ouputs = set(range(n_out)).difference(outputs_map)
    for endswith in [False, True]:
        if not unused_ouputs:
            return outputs_map

        for i in range(n_in):
            if outputs_map[i] is not None:
                continue
            cell_input = cells_inputs[i]
            for j in unused_ouputs:
                cell_output = cells_outputs[j]
                if cell_input.cell_type == cell_output.cell_type and same_content(
                    cell_output.source, cell_input.source, endswith
                ):
                    outputs_map[i] = j
                    unused_ouputs.remove(j)
                    break

    # Fourth rule: match based on increasing index (and cell type) for non-empty cells
    if not unused_ouputs:
        return outputs_map

    prev_j = -1
    for i in range(n_in):
        if outputs_map[i] is not None:
            prev_j = outputs_map[i]
            continue

        j = prev_j + 1
        if j not in unused_ouputs:
            continue

        cell_input = cells_inputs[i]
        cell_output = cells_outputs[j]
        if cell_input.cell_type == cell_output.cell_type and cell_input.source.strip() != "":
            outputs_map[i] = j
            unused_ouputs.remove(j)
            prev_j = j

    return outputs_map

