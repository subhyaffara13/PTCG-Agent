
def _iv_dunnett(
    samples: Sequence["npt.ArrayLike"],
    control: "npt.ArrayLike",
    alternative: Literal['two-sided', 'less', 'greater'],
    rng: SeedType
) -> tuple[list[np.ndarray], np.ndarray, SeedType]:
    """Input validation for Dunnett's test."""
    rng = check_random_state(rng)

    if alternative not in {'two-sided', 'less', 'greater'}:
        raise ValueError(
            "alternative must be 'less', 'greater' or 'two-sided'"
        )

    ndim_msg = "Control and samples groups must be 1D arrays"
    n_obs_msg = "Control and samples groups must have at least 1 observation"

    control = np.asarray(control)
    samples_ = [np.asarray(sample) for sample in samples]

    # samples checks
    samples_control: list[np.ndarray] = samples_ + [control]
    for sample in samples_control:
        if sample.ndim > 1:
            raise ValueError(ndim_msg)

        if sample.size < 1:
            raise ValueError(n_obs_msg)

    return samples_, control, rng

