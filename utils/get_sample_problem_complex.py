
def get_sample_problem_complex():
    A, b = _cached_sample_problem(True)
    return A.copy(), b.copy()

