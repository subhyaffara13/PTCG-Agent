
def _laplace_apply_prog_rules(f, t, s):
    """
    This function applies all program rules and returns the result if one
    of them gives a result.
    """

    prog_rules = [_laplace_rule_heaviside, _laplace_rule_delta,
                  _laplace_rule_timescale, _laplace_rule_exp,
                  _laplace_rule_trig,
                  _laplace_rule_diff, _laplace_rule_sdiff]

    for p_rule in prog_rules:
        if (L := p_rule(f, t, s)) is not None:
            return L
    return None

