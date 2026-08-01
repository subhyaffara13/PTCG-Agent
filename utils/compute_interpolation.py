
def compute_interpolation(x, y, kernel, epsilon, powers, shift, scale, coeffs, xp):
    vec = _build_evaluation_coefficients(
        x, y, kernel, epsilon, powers, shift, scale, xp
    )
    return vec @ coeffs


def compute_interpolation(x, y, kernel, epsilon, powers, shift, scale, coeffs, xp):
    vec = _build_evaluation_coefficients(
        x, y, kernel, epsilon, powers, shift, scale, xp
    )
    return vec @ coeffs

