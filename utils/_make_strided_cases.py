
def _make_strided_cases():
    new_cases = []
    for case in CASES:
        for a, a_label in _stride_comb_iter(case.a):
            for b, b_label in _stride_comb_iter(case.b):
                new_case = LinalgCase(case.name + "_" + a_label + "_" + b_label, a, b,
                                      tags=case.tags | {'strided'})
                new_cases.append(new_case)
    return new_cases

