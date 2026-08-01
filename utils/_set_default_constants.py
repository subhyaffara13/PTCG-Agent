
def _set_default_constants(**kwargs):
    """
    Set the default constants.
    """
    constants = dict(kwargs)
    constants.setdefault(
        Constants.DECREASE_RADIUS_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.DECREASE_RADIUS_FACTOR],
    )
    constants[Constants.DECREASE_RADIUS_FACTOR.value] = float(
        constants[Constants.DECREASE_RADIUS_FACTOR]
    )
    if (
        constants[Constants.DECREASE_RADIUS_FACTOR] <= 0.0
        or constants[Constants.DECREASE_RADIUS_FACTOR] >= 1.0
    ):
        raise ValueError(
            "The constant decrease_radius_factor must be in the interval "
            "(0, 1)."
        )
    constants.setdefault(
        Constants.INCREASE_RADIUS_THRESHOLD.value,
        DEFAULT_CONSTANTS[Constants.INCREASE_RADIUS_THRESHOLD],
    )
    constants[Constants.INCREASE_RADIUS_THRESHOLD.value] = float(
        constants[Constants.INCREASE_RADIUS_THRESHOLD]
    )
    if constants[Constants.INCREASE_RADIUS_THRESHOLD] <= 1.0:
        raise ValueError(
            "The constant increase_radius_threshold must be greater than 1."
        )
    if (
        Constants.INCREASE_RADIUS_FACTOR in constants
        and constants[Constants.INCREASE_RADIUS_FACTOR] <= 1.0
    ):
        raise ValueError(
            "The constant increase_radius_factor must be greater than 1."
        )
    if (
        Constants.DECREASE_RADIUS_THRESHOLD in constants
        and constants[Constants.DECREASE_RADIUS_THRESHOLD] <= 1.0
    ):
        raise ValueError(
            "The constant decrease_radius_threshold must be greater than 1."
        )
    if (
        Constants.INCREASE_RADIUS_FACTOR in constants
        and Constants.DECREASE_RADIUS_THRESHOLD in constants
    ):
        if (
            constants[Constants.DECREASE_RADIUS_THRESHOLD]
            >= constants[Constants.INCREASE_RADIUS_FACTOR]
        ):
            raise ValueError(
                "The constant decrease_radius_threshold must be "
                "less than increase_radius_factor."
            )
    elif Constants.INCREASE_RADIUS_FACTOR in constants:
        constants[Constants.DECREASE_RADIUS_THRESHOLD.value] = np.min(
            [
                DEFAULT_CONSTANTS[Constants.DECREASE_RADIUS_THRESHOLD],
                0.5 * (1.0 + constants[Constants.INCREASE_RADIUS_FACTOR]),
            ]
        )
    elif Constants.DECREASE_RADIUS_THRESHOLD in constants:
        constants[Constants.INCREASE_RADIUS_FACTOR.value] = np.max(
            [
                DEFAULT_CONSTANTS[Constants.INCREASE_RADIUS_FACTOR],
                2.0 * constants[Constants.DECREASE_RADIUS_THRESHOLD],
            ]
        )
    else:
        constants[Constants.INCREASE_RADIUS_FACTOR.value] = DEFAULT_CONSTANTS[
            Constants.INCREASE_RADIUS_FACTOR
        ]
        constants[Constants.DECREASE_RADIUS_THRESHOLD.value] = (
            DEFAULT_CONSTANTS[Constants.DECREASE_RADIUS_THRESHOLD])
    constants.setdefault(
        Constants.DECREASE_RESOLUTION_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.DECREASE_RESOLUTION_FACTOR],
    )
    constants[Constants.DECREASE_RESOLUTION_FACTOR.value] = float(
        constants[Constants.DECREASE_RESOLUTION_FACTOR]
    )
    if (
        constants[Constants.DECREASE_RESOLUTION_FACTOR] <= 0.0
        or constants[Constants.DECREASE_RESOLUTION_FACTOR] >= 1.0
    ):
        raise ValueError(
            "The constant decrease_resolution_factor must be in the interval "
            "(0, 1)."
        )
    if (
        Constants.LARGE_RESOLUTION_THRESHOLD in constants
        and constants[Constants.LARGE_RESOLUTION_THRESHOLD] <= 1.0
    ):
        raise ValueError(
            "The constant large_resolution_threshold must be greater than 1."
        )
    if (
        Constants.MODERATE_RESOLUTION_THRESHOLD in constants
        and constants[Constants.MODERATE_RESOLUTION_THRESHOLD] <= 1.0
    ):
        raise ValueError(
            "The constant moderate_resolution_threshold must be greater than "
            "1."
        )
    if (
        Constants.LARGE_RESOLUTION_THRESHOLD in constants
        and Constants.MODERATE_RESOLUTION_THRESHOLD in constants
    ):
        if (
            constants[Constants.MODERATE_RESOLUTION_THRESHOLD]
            > constants[Constants.LARGE_RESOLUTION_THRESHOLD]
        ):
            raise ValueError(
                "The constant moderate_resolution_threshold "
                "must be at most large_resolution_threshold."
            )
    elif Constants.LARGE_RESOLUTION_THRESHOLD in constants:
        constants[Constants.MODERATE_RESOLUTION_THRESHOLD.value] = np.min(
            [
                DEFAULT_CONSTANTS[Constants.MODERATE_RESOLUTION_THRESHOLD],
                constants[Constants.LARGE_RESOLUTION_THRESHOLD],
            ]
        )
    elif Constants.MODERATE_RESOLUTION_THRESHOLD in constants:
        constants[Constants.LARGE_RESOLUTION_THRESHOLD.value] = np.max(
            [
                DEFAULT_CONSTANTS[Constants.LARGE_RESOLUTION_THRESHOLD],
                constants[Constants.MODERATE_RESOLUTION_THRESHOLD],
            ]
        )
    else:
        constants[Constants.LARGE_RESOLUTION_THRESHOLD.value] = (
            DEFAULT_CONSTANTS[Constants.LARGE_RESOLUTION_THRESHOLD]
        )
        constants[Constants.MODERATE_RESOLUTION_THRESHOLD.value] = (
            DEFAULT_CONSTANTS[Constants.MODERATE_RESOLUTION_THRESHOLD]
        )
    if Constants.LOW_RATIO in constants and (
        constants[Constants.LOW_RATIO] <= 0.0
        or constants[Constants.LOW_RATIO] >= 1.0
    ):
        raise ValueError(
            "The constant low_ratio must be in the interval (0, 1)."
        )
    if Constants.HIGH_RATIO in constants and (
        constants[Constants.HIGH_RATIO] <= 0.0
        or constants[Constants.HIGH_RATIO] >= 1.0
    ):
        raise ValueError(
            "The constant high_ratio must be in the interval (0, 1)."
        )
    if Constants.LOW_RATIO in constants and Constants.HIGH_RATIO in constants:
        if constants[Constants.LOW_RATIO] > constants[Constants.HIGH_RATIO]:
            raise ValueError(
                "The constant low_ratio must be at most high_ratio."
            )
    elif Constants.LOW_RATIO in constants:
        constants[Constants.HIGH_RATIO.value] = np.max(
            [
                DEFAULT_CONSTANTS[Constants.HIGH_RATIO],
                constants[Constants.LOW_RATIO],
            ]
        )
    elif Constants.HIGH_RATIO in constants:
        constants[Constants.LOW_RATIO.value] = np.min(
            [
                DEFAULT_CONSTANTS[Constants.LOW_RATIO],
                constants[Constants.HIGH_RATIO],
            ]
        )
    else:
        constants[Constants.LOW_RATIO.value] = DEFAULT_CONSTANTS[
            Constants.LOW_RATIO
        ]
        constants[Constants.HIGH_RATIO.value] = DEFAULT_CONSTANTS[
            Constants.HIGH_RATIO
        ]
    constants.setdefault(
        Constants.VERY_LOW_RATIO.value,
        DEFAULT_CONSTANTS[Constants.VERY_LOW_RATIO],
    )
    constants[Constants.VERY_LOW_RATIO.value] = float(
        constants[Constants.VERY_LOW_RATIO]
    )
    if (
        constants[Constants.VERY_LOW_RATIO] <= 0.0
        or constants[Constants.VERY_LOW_RATIO] >= 1.0
    ):
        raise ValueError(
            "The constant very_low_ratio must be in the interval (0, 1)."
        )
    if (
        Constants.PENALTY_INCREASE_THRESHOLD in constants
        and constants[Constants.PENALTY_INCREASE_THRESHOLD] < 1.0
    ):
        raise ValueError(
            "The constant penalty_increase_threshold must be "
            "greater than or equal to 1."
        )
    if (
        Constants.PENALTY_INCREASE_FACTOR in constants
        and constants[Constants.PENALTY_INCREASE_FACTOR] <= 1.0
    ):
        raise ValueError(
            "The constant penalty_increase_factor must be greater than 1."
        )
    if (
        Constants.PENALTY_INCREASE_THRESHOLD in constants
        and Constants.PENALTY_INCREASE_FACTOR in constants
    ):
        if (
            constants[Constants.PENALTY_INCREASE_FACTOR]
            < constants[Constants.PENALTY_INCREASE_THRESHOLD]
        ):
            raise ValueError(
                "The constant penalty_increase_factor must be "
                "greater than or equal to "
                "penalty_increase_threshold."
            )
    elif Constants.PENALTY_INCREASE_THRESHOLD in constants:
        constants[Constants.PENALTY_INCREASE_FACTOR.value] = np.max(
            [
                DEFAULT_CONSTANTS[Constants.PENALTY_INCREASE_FACTOR],
                constants[Constants.PENALTY_INCREASE_THRESHOLD],
            ]
        )
    elif Constants.PENALTY_INCREASE_FACTOR in constants:
        constants[Constants.PENALTY_INCREASE_THRESHOLD.value] = np.min(
            [
                DEFAULT_CONSTANTS[Constants.PENALTY_INCREASE_THRESHOLD],
                constants[Constants.PENALTY_INCREASE_FACTOR],
            ]
        )
    else:
        constants[Constants.PENALTY_INCREASE_THRESHOLD.value] = (
            DEFAULT_CONSTANTS[Constants.PENALTY_INCREASE_THRESHOLD]
        )
        constants[Constants.PENALTY_INCREASE_FACTOR.value] = DEFAULT_CONSTANTS[
            Constants.PENALTY_INCREASE_FACTOR
        ]
    constants.setdefault(
        Constants.SHORT_STEP_THRESHOLD.value,
        DEFAULT_CONSTANTS[Constants.SHORT_STEP_THRESHOLD],
    )
    constants[Constants.SHORT_STEP_THRESHOLD.value] = float(
        constants[Constants.SHORT_STEP_THRESHOLD]
    )
    if (
        constants[Constants.SHORT_STEP_THRESHOLD] <= 0.0
        or constants[Constants.SHORT_STEP_THRESHOLD] >= 1.0
    ):
        raise ValueError(
            "The constant short_step_threshold must be in the interval (0, 1)."
        )
    constants.setdefault(
        Constants.LOW_RADIUS_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.LOW_RADIUS_FACTOR],
    )
    constants[Constants.LOW_RADIUS_FACTOR.value] = float(
        constants[Constants.LOW_RADIUS_FACTOR]
    )
    if (
        constants[Constants.LOW_RADIUS_FACTOR] <= 0.0
        or constants[Constants.LOW_RADIUS_FACTOR] >= 1.0
    ):
        raise ValueError(
            "The constant low_radius_factor must be in the interval (0, 1)."
        )
    constants.setdefault(
        Constants.BYRD_OMOJOKUN_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.BYRD_OMOJOKUN_FACTOR],
    )
    constants[Constants.BYRD_OMOJOKUN_FACTOR.value] = float(
        constants[Constants.BYRD_OMOJOKUN_FACTOR]
    )
    if (
        constants[Constants.BYRD_OMOJOKUN_FACTOR] <= 0.0
        or constants[Constants.BYRD_OMOJOKUN_FACTOR] >= 1.0
    ):
        raise ValueError(
            "The constant byrd_omojokun_factor must be in the interval (0, 1)."
        )
    constants.setdefault(
        Constants.THRESHOLD_RATIO_CONSTRAINTS.value,
        DEFAULT_CONSTANTS[Constants.THRESHOLD_RATIO_CONSTRAINTS],
    )
    constants[Constants.THRESHOLD_RATIO_CONSTRAINTS.value] = float(
        constants[Constants.THRESHOLD_RATIO_CONSTRAINTS]
    )
    if constants[Constants.THRESHOLD_RATIO_CONSTRAINTS] <= 1.0:
        raise ValueError(
            "The constant threshold_ratio_constraints must be greater than 1."
        )
    constants.setdefault(
        Constants.LARGE_SHIFT_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.LARGE_SHIFT_FACTOR],
    )
    constants[Constants.LARGE_SHIFT_FACTOR.value] = float(
        constants[Constants.LARGE_SHIFT_FACTOR]
    )
    if constants[Constants.LARGE_SHIFT_FACTOR] < 0.0:
        raise ValueError("The constant large_shift_factor must be "
                         "nonnegative.")
    constants.setdefault(
        Constants.LARGE_GRADIENT_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.LARGE_GRADIENT_FACTOR],
    )
    constants[Constants.LARGE_GRADIENT_FACTOR.value] = float(
        constants[Constants.LARGE_GRADIENT_FACTOR]
    )
    if constants[Constants.LARGE_GRADIENT_FACTOR] <= 1.0:
        raise ValueError(
            "The constant large_gradient_factor must be greater than 1."
        )
    constants.setdefault(
        Constants.RESOLUTION_FACTOR.value,
        DEFAULT_CONSTANTS[Constants.RESOLUTION_FACTOR],
    )
    constants[Constants.RESOLUTION_FACTOR.value] = float(
        constants[Constants.RESOLUTION_FACTOR]
    )
    if constants[Constants.RESOLUTION_FACTOR] <= 1.0:
        raise ValueError(
            "The constant resolution_factor must be greater than 1."
        )
    constants.setdefault(
        Constants.IMPROVE_TCG.value,
        DEFAULT_CONSTANTS[Constants.IMPROVE_TCG],
    )
    constants[Constants.IMPROVE_TCG.value] = bool(
        constants[Constants.IMPROVE_TCG]
    )

    # Check whether they are any unknown options.
    for key in kwargs:
        if key not in Constants.__members__.values():
            warnings.warn(f"Unknown constant: {key}.", RuntimeWarning, 3)
    return constants

