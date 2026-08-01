
def _rel_entr(xp, spsx):
    def __rel_entr(x, y, *, xp=xp):
        # https://github.com/data-apis/array-api-extra/issues/160
        mxp = array_namespace(x._meta, y._meta) if is_dask(xp) else xp
        x, y = xp_promote(x, y, broadcast=True, force_floating=True, xp=xp)
        xy_pos = (x > 0) & (y > 0)
        xy_inf = xp.isinf(x) & xp.isinf(y)
        res = xpx.apply_where(
            xy_pos & ~xy_inf,
            (x, y),
            # Note: for very large x, this can overflow.
            lambda x, y: x * (mxp.log(x) - mxp.log(y)),
            fill_value=xp.inf
        )
        res = xpx.at(res)[(x == 0) & (y >= 0)].set(0)
        res = xpx.at(res)[xp.isnan(x) | xp.isnan(y) | (xy_pos & xy_inf)].set(xp.nan)
        return res

    return __rel_entr

