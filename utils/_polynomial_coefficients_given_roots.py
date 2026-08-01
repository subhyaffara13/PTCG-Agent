
def _polynomial_coefficients_given_roots(roots):
    """
    Given the `roots` of a polynomial, find the polynomial's coefficients.

    If roots = (r_1, ..., r_n), then the method returns
    coefficients (a_0, a_1, ..., a_n (== 1)) so that
    p(x) = (x - r_1) * ... * (x - r_n)
         = x^n + a_{n-1} * x^{n-1} + ... a_1 * x_1 + a_0

    Note: for better performance requires writing a low-level kernel
    """
    poly_order = roots.shape[-1]
    poly_coeffs_shape = list(roots.shape)
    # we assume p(x) = x^n + a_{n-1} * x^{n-1} + ... + a_1 * x + a_0,
    # so poly_coeffs = {a_0, ..., a_n, a_{n+1}(== 1)},
    # but we insert one extra coefficient to enable better vectorization below
    poly_coeffs_shape[-1] += 2
    poly_coeffs = roots.new_zeros(poly_coeffs_shape)
    poly_coeffs[..., 0] = 1
    poly_coeffs[..., -1] = 1

    # perform the Horner's rule
    for i in range(1, poly_order + 1):
        # note that it is computationally hard to compute backward for this method,
        # because then given the coefficients it would require finding the roots and/or
        # calculating the sensitivity based on the Vieta's theorem.
        # So the code below tries to circumvent the explicit root finding by series
        # of operations on memory copies imitating the Horner's method.
        # The memory copies are required to construct nodes in the computational graph
        # by exploiting the explicit (not in-place, separate node for each step)
        # recursion of the Horner's method.
        # Needs more memory, O(... * k^2), but with only O(... * k^2) complexity.
        poly_coeffs_new = poly_coeffs.clone() if roots.requires_grad else poly_coeffs
        out = poly_coeffs_new.narrow(-1, poly_order - i, i + 1)
        out -= roots.narrow(-1, i - 1, 1) * poly_coeffs.narrow(
            -1, poly_order - i + 1, i + 1
        )
        poly_coeffs = poly_coeffs_new

    return poly_coeffs.narrow(-1, 1, poly_order + 1)

