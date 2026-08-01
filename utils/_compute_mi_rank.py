
def _compute_mi_rank(score):
    if 0 <= score < 10:
        res = 'C'
    elif 10 <= score < 20:
        res = 'B'
    elif 20 <= score <= 100:
        res = 'A'
    else:
        raise ValueError(score)
    return res

