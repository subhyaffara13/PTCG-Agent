
def _make_generalized_cases():
    new_cases = []

    for case in CASES:
        if not isinstance(case.a, np.ndarray):
            continue

        a = np.array([case.a, 2 * case.a, 3 * case.a])
        if case.b is None:
            b = None
        elif case.b.ndim == 1:
            b = case.b
        else:
            b = np.array([case.b, 7 * case.b, 6 * case.b])
        new_case = LinalgCase(case.name + "_tile3", a, b,
                              tags=case.tags | {'generalized'})
        new_cases.append(new_case)

        a = np.array([case.a] * 2 * 3).reshape((3, 2) + case.a.shape)
        if case.b is None:
            b = None
        elif case.b.ndim == 1:
            b = np.array([case.b] * 2 * 3 * a.shape[-1])\
                  .reshape((3, 2) + case.a.shape[-2:])
        else:
            b = np.array([case.b] * 2 * 3).reshape((3, 2) + case.b.shape)
        new_case = LinalgCase(case.name + "_tile213", a, b,
                              tags=case.tags | {'generalized'})
        new_cases.append(new_case)

    return new_cases

