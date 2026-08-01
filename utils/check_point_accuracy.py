
def check_point_accuracy(a, b):
    return all(isclose(*_, rel_tol=1e-1, abs_tol=1e-6
        ) for _ in zip(a, b))

