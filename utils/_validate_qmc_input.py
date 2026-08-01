
def _validate_qmc_input(qmc_engine, d, seed):
    # Input validation for `qmc_engine` and `d`
    # Error messages for invalid `d` are raised by QMCEngine
    # we could probably use a stats.qmc.check_qrandom_state
    if isinstance(qmc_engine, QMCEngine):
        if d is not None and qmc_engine.d != d:
            message = "`d` must be consistent with dimension of `qmc_engine`."
            raise ValueError(message)
        d = qmc_engine.d if d is None else d
    elif qmc_engine is None:
        d = 1 if d is None else d
        qmc_engine = Halton(d, seed=seed)
    else:
        message = (
            "`qmc_engine` must be an instance of "
            "`scipy.stats.qmc.QMCEngine` or `None`."
        )
        raise ValueError(message)

    return qmc_engine, d

