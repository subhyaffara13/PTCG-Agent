
def _to_mat(pairs: list[tuple[str, int]]) -> np.ndarray:
    mat = np.zeros((4, 4))
    for key, value in pairs:
        ind = _qtr_ind_dict[key]
        mat[ind // 4][ind % 4] = value

    return mat

