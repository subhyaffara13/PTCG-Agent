
def _set_default_options(options, n):
    """
    Set the default options.
    """
    if Options.RHOBEG in options and options[Options.RHOBEG] <= 0.0:
        raise ValueError("The initial trust-region radius must be positive.")
    if Options.RHOEND in options and options[Options.RHOEND] < 0.0:
        raise ValueError("The final trust-region radius must be nonnegative.")
    if Options.RHOBEG in options and Options.RHOEND in options:
        if options[Options.RHOBEG] < options[Options.RHOEND]:
            raise ValueError(
                "The initial trust-region radius must be greater "
                "than or equal to the final trust-region radius."
            )
    elif Options.RHOBEG in options:
        options[Options.RHOEND.value] = np.min(
            [
                DEFAULT_OPTIONS[Options.RHOEND],
                options[Options.RHOBEG],
            ]
        )
    elif Options.RHOEND in options:
        options[Options.RHOBEG.value] = np.max(
            [
                DEFAULT_OPTIONS[Options.RHOBEG],
                options[Options.RHOEND],
            ]
        )
    else:
        options[Options.RHOBEG.value] = DEFAULT_OPTIONS[Options.RHOBEG]
        options[Options.RHOEND.value] = DEFAULT_OPTIONS[Options.RHOEND]
    options[Options.RHOBEG.value] = float(options[Options.RHOBEG])
    options[Options.RHOEND.value] = float(options[Options.RHOEND])
    if Options.NPT in options and options[Options.NPT] <= 0:
        raise ValueError("The number of interpolation points must be "
                         "positive.")
    if (
        Options.NPT in options
        and options[Options.NPT] > ((n + 1) * (n + 2)) // 2
    ):
        raise ValueError(
            f"The number of interpolation points must be at most "
            f"{((n + 1) * (n + 2)) // 2}."
        )
    options.setdefault(Options.NPT.value, DEFAULT_OPTIONS[Options.NPT](n))
    options[Options.NPT.value] = int(options[Options.NPT])
    if Options.MAX_EVAL in options and options[Options.MAX_EVAL] <= 0:
        raise ValueError(
            "The maximum number of function evaluations must be positive."
        )
    options.setdefault(
        Options.MAX_EVAL.value,
        np.max(
            [
                DEFAULT_OPTIONS[Options.MAX_EVAL](n),
                options[Options.NPT] + 1,
            ]
        ),
    )
    options[Options.MAX_EVAL.value] = int(options[Options.MAX_EVAL])
    if Options.MAX_ITER in options and options[Options.MAX_ITER] <= 0:
        raise ValueError("The maximum number of iterations must be positive.")
    options.setdefault(
        Options.MAX_ITER.value,
        DEFAULT_OPTIONS[Options.MAX_ITER](n),
    )
    options[Options.MAX_ITER.value] = int(options[Options.MAX_ITER])
    options.setdefault(Options.TARGET.value, DEFAULT_OPTIONS[Options.TARGET])
    options[Options.TARGET.value] = float(options[Options.TARGET])
    options.setdefault(
        Options.FEASIBILITY_TOL.value,
        DEFAULT_OPTIONS[Options.FEASIBILITY_TOL],
    )
    options[Options.FEASIBILITY_TOL.value] = float(
        options[Options.FEASIBILITY_TOL]
    )
    options.setdefault(Options.VERBOSE.value, DEFAULT_OPTIONS[Options.VERBOSE])
    options[Options.VERBOSE.value] = bool(options[Options.VERBOSE])
    options.setdefault(Options.SCALE.value, DEFAULT_OPTIONS[Options.SCALE])
    options[Options.SCALE.value] = bool(options[Options.SCALE])
    options.setdefault(
        Options.FILTER_SIZE.value,
        DEFAULT_OPTIONS[Options.FILTER_SIZE],
    )
    options[Options.FILTER_SIZE.value] = int(options[Options.FILTER_SIZE])
    options.setdefault(
        Options.STORE_HISTORY.value,
        DEFAULT_OPTIONS[Options.STORE_HISTORY],
    )
    options[Options.STORE_HISTORY.value] = bool(options[Options.STORE_HISTORY])
    options.setdefault(
        Options.HISTORY_SIZE.value,
        DEFAULT_OPTIONS[Options.HISTORY_SIZE],
    )
    options[Options.HISTORY_SIZE.value] = int(options[Options.HISTORY_SIZE])
    options.setdefault(Options.DEBUG.value, DEFAULT_OPTIONS[Options.DEBUG])
    options[Options.DEBUG.value] = bool(options[Options.DEBUG])

    # Check whether they are any unknown options.
    for key in options:
        if key not in Options.__members__.values():
            warnings.warn(f"Unknown option: {key}.", RuntimeWarning, 3)

