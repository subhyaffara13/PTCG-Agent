
def _get_candidate_for_matmul_from_contraction(scan_indices: list[int | None], remaining_args: list[_ArgE]) -> tuple[_ArgE | None, bool, int]:

    scan_indices_int: list[int] = [i for i in scan_indices if i is not None]
    if len(scan_indices_int) == 0:
        return None, False, -1

    transpose: bool = False
    candidate: _ArgE | None = None
    candidate_index: int = -1
    for arg_with_ind2 in remaining_args:
        if not isinstance(arg_with_ind2.element, MatrixExpr):
            continue
        for index in scan_indices_int:
            if candidate_index != -1 and candidate_index != index:
                # A candidate index has already been selected, check
                # repetitions only for that index:
                continue
            if index in arg_with_ind2.indices:
                if set(arg_with_ind2.indices) == {index}:
                    # Index repeated twice in arg_with_ind2
                    candidate = None
                    break
                if candidate is None:
                    candidate = arg_with_ind2
                    candidate_index = index
                    transpose = (index == arg_with_ind2.indices[1])
                else:
                    # Index repeated more than twice, break
                    candidate = None
                    break
    return candidate, transpose, candidate_index

