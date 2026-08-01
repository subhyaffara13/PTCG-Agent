
def _remove_diagonalized_identity_matrices(expr: ArrayDiagonal):
    assert isinstance(expr, ArrayDiagonal)
    editor = _EditArrayContraction(expr)
    mapping = {i: {j for j in editor.args_with_ind if i in j.indices} for i in range(-1, -1-editor.number_of_diagonal_indices, -1)}
    removed = []
    counter: int = 0
    for i, arg_with_ind in enumerate(editor.args_with_ind):
        counter += len(arg_with_ind.indices)
        if isinstance(arg_with_ind.element, Identity):
            if None in arg_with_ind.indices and any(i is not None and (i < 0) == True for i in arg_with_ind.indices):
                diag_ind = [j for j in arg_with_ind.indices if j is not None][0]
                other = [j for j in mapping[diag_ind] if j != arg_with_ind][0]
                if not isinstance(other.element, MatrixExpr):
                    continue
                if 1 not in other.element.shape:
                    continue
                if None not in other.indices:
                    continue
                editor.args_with_ind[i].element = None
                none_index = other.indices.index(None)
                other.element = DiagMatrix(other.element)
                other_range = editor.get_absolute_range(other)
                removed.extend([other_range[0] + none_index])
    editor.args_with_ind = [i for i in editor.args_with_ind if i.element is not None]
    removed = ArrayDiagonal._push_indices_up(expr.diagonal_indices, removed, get_rank(expr.expr))
    return editor.to_array_contraction(), removed

