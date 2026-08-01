
def concat_1d(xp: ModuleType | None, *arrays: Iterable[ArrayLike]) -> Array:
    """A replacement for `np.r_` as `xp.concat` does not accept python scalars
       or 0-D arrays.
    """
    arys = [xpx.atleast_nd(xp.asarray(a), ndim=1, xp=xp) for a in arrays]  # type:ignore[union-attr]
    return xp.concat(arys)  # type:ignore[union-attr]

