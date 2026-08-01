
def _gof_iv(dist, data, known_params, fit_params, guessed_params, statistic,
            n_mc_samples, rng):

    if not isinstance(dist, stats.rv_continuous):
        message = ("`dist` must be a (non-frozen) instance of "
                   "`stats.rv_continuous`.")
        raise TypeError(message)

    data = np.asarray(data, dtype=float)
    if not data.ndim == 1:
        message = "`data` must be a one-dimensional array of numbers."
        raise ValueError(message)

    # Leave validation of these key/value pairs to the `fit` method,
    # but collect these into dictionaries that will be used
    known_params = known_params or dict()
    fit_params = fit_params or dict()
    guessed_params = guessed_params or dict()

    known_params_f = {("f"+key): val for key, val in known_params.items()}
    fit_params_f = {("f"+key): val for key, val in fit_params.items()}

    # These are the values of parameters of the null distribution family
    # with which resamples are drawn
    fixed_nhd_params = known_params_f.copy()
    fixed_nhd_params.update(fit_params_f)

    # These are fixed when fitting the distribution family to resamples
    fixed_rfd_params = known_params_f.copy()

    # These are used as guesses when fitting the distribution family to
    # the original data
    guessed_nhd_params = guessed_params.copy()

    # These are used as guesses when fitting the distribution family to
    # resamples
    guessed_rfd_params = fit_params.copy()
    guessed_rfd_params.update(guessed_params)

    if not callable(statistic):
        statistic = statistic.lower()
        statistics = {'ad', 'ks', 'cvm', 'filliben'}
        if statistic not in statistics:
            message = f"`statistic` must be one of {statistics}."
            raise ValueError(message)

    n_mc_samples_int = int(n_mc_samples)
    if n_mc_samples_int != n_mc_samples:
        message = "`n_mc_samples` must be an integer."
        raise TypeError(message)

    rng = check_random_state(rng)

    return (dist, data, fixed_nhd_params, fixed_rfd_params, guessed_nhd_params,
            guessed_rfd_params, statistic, n_mc_samples_int, rng)

