
def remove_identity_matrices(expr: ArrayContraction):
    editor = _EditArrayContraction(expr)
    removed: list[int] = []

    permutation_map = {}

    free_indices = list(accumulate([0] + [sum(i is None for i in arg.indices) for arg in editor.args_with_ind]))
    free_map = dict(zip(editor.args_with_ind, free_indices[:-1]))

    update_pairs = {}

    for ind in range(editor.number_of_contraction_indices):
        args = editor.get_args_with_index(ind)
        identity_matrices = [i for i in args if isinstance(i.element, Identity)]
        number_identity_matrices = len(identity_matrices)
        # If the contraction involves a non-identity matrix and multiple identity matrices:
        if number_identity_matrices != len(args) - 1 or number_identity_matrices == 0:
            continue
        # Get the non-identity element:
        non_identity = [i for i in args if not isinstance(i.element, Identity)][0]
        # Check that all identity matrices have at least one free index
        # (otherwise they would be contractions to some other elements)
        if any(None not in i.indices for i in identity_matrices):
            continue
        # Mark the identity matrices for removal:
        for i in identity_matrices:
            i.element = None
            removed.extend(range(free_map[i], free_map[i] + len([j for j in i.indices if j is None])))
        last_removed = removed.pop(-1)
        update_pairs[last_removed, ind] = non_identity.indices[:]
        # Remove the indices from the non-identity matrix, as the contraction
        # no longer exists:
        non_identity.indices = [None if i == ind else i for i in non_identity.indices]

    removed.sort()

    shifts = list(accumulate([1 if i in removed else 0 for i in range(get_rank(expr))]))
    for (last_removed, ind), non_identity_indices in update_pairs.items():
        pos = [free_map[non_identity] + i for i, e in enumerate(non_identity_indices) if e == ind]
        assert len(pos) == 1
        for j in pos:
            permutation_map[j] = last_removed

    editor.args_with_ind = [i for i in editor.args_with_ind if i.element is not None]
    ret_expr = editor.to_array_contraction()
    permutation = []
    counter = 0
    counter2 = 0
    for j in range(get_rank(expr)):
        if j in removed:
            continue
        if counter2 in permutation_map:
            target = permutation_map[counter2]
            permutation.append(target - shifts[target])
            counter2 += 1
        else:
            while counter in permutation_map.values():
                counter += 1
            permutation.append(counter)
            counter += 1
            counter2 += 1
    ret_expr2 = _permute_dims(ret_expr, _af_invert(permutation))
    return ret_expr2, removed

