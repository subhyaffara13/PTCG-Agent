
def _vector_polynomial_value(poly, x, zero_power=None):
    """
    Evaluates `poly(x)` for the (batched) vector input `x`.
    Check out `_polynomial_value` function for more details.
    """

    # vector-aware Horner's rule iteration
    def transition(curr_poly_val, x, poly_coeff):
        res = torch.addcmul(poly_coeff.unsqueeze(-1), x, curr_poly_val)
        return res

    if zero_power is None:
        zero_power = x.new_ones(1).expand(x.shape)

    return _polynomial_value(poly, x, zero_power, transition)

