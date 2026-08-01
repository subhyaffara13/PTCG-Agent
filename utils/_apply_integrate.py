
def _apply_integrate(sol, x, k):
    return [(res / ((cond + 1)*(cond.as_coeff_Add()[1].coeff(k))), cond + 1)
            for res, cond in sol]

