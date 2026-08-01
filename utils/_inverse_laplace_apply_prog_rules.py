
def _inverse_laplace_apply_prog_rules(F, s, t, plane):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    prog_rules = [_inverse_laplace_time_shift, _inverse_laplace_freq_shift,
                  _inverse_laplace_time_diff, _inverse_laplace_diff,
                  _inverse_laplace_irrational]

    for p_rule in prog_rules:
        if (r := p_rule(F, s, t, plane)) is not None:
            return r
    return None

