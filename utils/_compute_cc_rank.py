
def _compute_cc_rank(score):
    # This is really ugly
    # Luckily the rank function in radon.complexity is not like this!
    if score < 0:
        rank = ValueError
    elif 0 <= score <= 5:
        rank = 'A'
    elif 6 <= score <= 10:
        rank = 'B'
    elif 11 <= score <= 20:
        rank = 'C'
    elif 21 <= score <= 30:
        rank = 'D'
    elif 31 <= score <= 40:
        rank = 'E'
    else:
        rank = 'F'
    return rank

