
def _append_contraction_marks_sub(Z, iv, i, n, contraction_marks, xp):
    if i >= n:
        contraction_marks.append((iv, Z[i - n, 2]))
        _append_contraction_marks_sub(Z, iv, _int_floor(Z[i - n, 0], xp),
                                      n, contraction_marks, xp)
        _append_contraction_marks_sub(Z, iv, _int_floor(Z[i - n, 1], xp),
                                      n, contraction_marks, xp)

