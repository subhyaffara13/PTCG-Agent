
def _lax_max_taylor_rule(primal_in, series_in):
    x, y = jnp.broadcast_arrays(*primal_in)

    xgy = x > y   # greater than mask
    xey = x == y  # equal to mask
    primal_out = lax.select(xgy, x, y)

    def select_max_and_avg_eq(x_i, y_i):
        """Select x where x>y or average when x==y"""
        max_i = lax.select(xgy, x_i, y_i)
        max_i = lax.select(xey, (x_i + y_i)/2, max_i)
        return max_i

    series_out = [select_max_and_avg_eq(*jnp.broadcast_arrays(*terms_in)) for terms_in in zip(*series_in)]
    return primal_out, series_out

