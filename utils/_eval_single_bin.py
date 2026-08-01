
def _eval_single_bin(lhs, cmp1, rhs, engine):
    c = _binary_ops_dict[cmp1]
    if ENGINES[engine].has_neg_frac:
        try:
            return c(lhs, rhs)
        except ValueError as e:
            if str(e).startswith(
                "negative number cannot be raised to a fractional power"
            ):
                return np.nan
            raise
    return c(lhs, rhs)

