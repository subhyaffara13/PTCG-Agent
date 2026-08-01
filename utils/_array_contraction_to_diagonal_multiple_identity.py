
def _array_contraction_to_diagonal_multiple_identity(expr: ArrayContraction):
    editor = _EditArrayContraction(expr)
    editor.track_permutation_start()
    removed: list[int] = []
    diag_index_counter: int = 0
    for i in range(editor.number_of_contraction_indices):
        identities = []
        args = []
        for j, arg in enumerate(editor.args_with_ind):
            if i not in arg.indices:
                continue
            if isinstance(arg.element, Identity):
                identities.append(arg)
            else:
                args.append(arg)
        if len(identities) == 0:
            continue
        if len(args) + len(identities) < 3:
            continue
        new_diag_ind = -1 - diag_index_counter
        diag_index_counter += 1
        # Variable "flag" to control whether to skip this contraction set:
        flag: bool = True
        for i1, id1 in enumerate(identities):
            if None not in id1.indices:
                flag = True
                break
            free_pos = list(range(*editor.get_absolute_free_range(id1)))[0]
            editor._track_permutation[-1].append(free_pos) # type: ignore
            id1.element = None
            flag = False
            break
        if flag:
            continue
        for arg in identities[:i1] + identities[i1+1:]:
            arg.element = None
            removed.extend(range(*editor.get_absolute_free_range(arg)))
        for arg in args:
            arg.indices = [new_diag_ind if j == i else j for j in arg.indices]
    for j, e in enumerate(editor.args_with_ind):
        if e.element is None:
            editor._track_permutation[j] = None # type: ignore
    editor._track_permutation = [i for i in editor._track_permutation if i is not None] # type: ignore
    # Renumber permutation array form in order to deal with deleted positions:
    remap = {e: i for i, e in enumerate(sorted({k for j in editor._track_permutation for k in j}))}
    editor._track_permutation = [[remap[j] for j in i] for i in editor._track_permutation]
    editor.args_with_ind = [i for i in editor.args_with_ind if i.element is not None]
    new_expr = editor.to_array_contraction()
    return new_expr, removed

