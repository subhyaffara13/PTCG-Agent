
def _matrix_polynomial_value(poly, x, zero_power=None):
    """
    Evaluates `poly(x)` for the (batched) matrix input `x`.
    Check out `_polynomial_value` function for more details.
    """

    # matrix-aware Horner's rule iteration
    def transition(curr_poly_val, x, poly_coeff):
        res = x.matmul(curr_poly_val)
        res.diagonal(dim1=-2, dim2=-1).add_(poly_coeff.unsqueeze(-1))
        return res

    if zero_power is None:
        zero_power = torch.eye(
            x.size(-1), x.size(-1), dtype=x.dtype, device=x.device
        ).view(*([1] * len(list(x.shape[:-2]))), x.size(-1), x.size(-1))

    return _polynomial_value(poly, x, zero_power, transition)

