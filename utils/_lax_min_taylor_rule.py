
def _lax_min_taylor_rule(primal_in, series_in):
    x, y = primal_in
    xgy = x < y   # less than mask
    xey = x == y  # equal to mask
    primal_out = lax.select(xgy, x, y)

    def select_min_and_avg_eq(x_i, y_i):
        """Select x where x>y or average when x==y"""
        min_i = lax.select(xgy, x_i, y_i)
        min_i = lax.select(xey, (x_i + y_i)/2, min_i)
        return min_i

    series_out = [select_min_and_avg_eq(*terms_in) for terms_in in zip(*series_in)]
    return primal_out, series_out

