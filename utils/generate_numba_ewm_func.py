
def generate_numba_ewm_func(
    nopython: bool,
    nogil: bool,
    parallel: bool,
    com: float,
    adjust: bool,
    ignore_na: bool,
    deltas: tuple,
    normalize: bool,
):
    """
    Generate a numba jitted ewm mean or sum function specified by values
    from engine_kwargs.

    Parameters
    ----------
    nopython : bool
        nopython to be passed into numba.jit
    nogil : bool
        nogil to be passed into numba.jit
    parallel : bool
        parallel to be passed into numba.jit
    com : float
    adjust : bool
    ignore_na : bool
    deltas : tuple
    normalize : bool

    Returns
    -------
    Numba function
    """
    if TYPE_CHECKING:
        import numba
    else:
        numba = import_optional_dependency("numba")

    @numba.jit(nopython=nopython, nogil=nogil, parallel=parallel)
    def ewm(
        values: np.ndarray,
        begin: np.ndarray,
        end: np.ndarray,
        minimum_periods: int,
    ) -> np.ndarray:
        result = np.empty(len(values))
        alpha = 1.0 / (1.0 + com)
        old_wt_factor = 1.0 - alpha
        new_wt = 1.0 if adjust else alpha

        for i in numba.prange(len(begin)):
            start = begin[i]
            stop = end[i]
            window = values[start:stop]
            sub_result = np.empty(len(window))

            weighted = window[0]
            nobs = int(not np.isnan(weighted))
            sub_result[0] = weighted if nobs >= minimum_periods else np.nan
            old_wt = 1.0

            for j in range(1, len(window)):
                cur = window[j]
                is_observation = not np.isnan(cur)
                nobs += is_observation
                if not np.isnan(weighted):
                    if is_observation or not ignore_na:
                        if normalize:
                            # note that len(deltas) = len(vals) - 1 and deltas[i]
                            # is to be used in conjunction with vals[i+1]
                            old_wt *= old_wt_factor ** deltas[start + j - 1]
                            if not adjust and com == 1:
                                # update in case of irregular-interval time series
                                new_wt = 1.0 - old_wt
                        else:
                            weighted = old_wt_factor * weighted
                        if is_observation:
                            if normalize:
                                # avoid numerical errors on constant series
                                if weighted != cur:
                                    weighted = old_wt * weighted + new_wt * cur
                                    if normalize:
                                        weighted = weighted / (old_wt + new_wt)
                                if adjust:
                                    old_wt += new_wt
                                else:
                                    old_wt = 1.0
                            else:
                                weighted += cur
                elif is_observation:
                    weighted = cur

                sub_result[j] = weighted if nobs >= minimum_periods else np.nan

            result[start:stop] = sub_result

        return result

    return ewm

