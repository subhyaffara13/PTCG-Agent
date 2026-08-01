
def calculate_equalization_scale(
    input_obs: _InputEqualizationObserver, weight_obs: _WeightEqualizationObserver
) -> torch.Tensor:
    r"""Calculates the equalization scale and sets the equalization_scale value
    in the observers.

    Args:
        input_obs: Observer that tracks the ranges for the input columns
        weight_obs: Observer that tracks the ranges for the weight columns
    """

    (min_inputs, max_inputs) = input_obs.get_input_minmax()
    (min_weights, max_weights) = weight_obs.get_weight_col_minmax()

    if not (
        check_min_max_valid(min_inputs, max_inputs)
        and check_min_max_valid(min_weights, max_weights)
    ):
        warnings.warn(
            "Must run observer before calling calculate_equalization_scale. "
            + "Returning default equalization scale torch.tensor(1).",
            stacklevel=2,
        )
        return torch.tensor(1)

    if min_inputs.shape != min_weights.shape:
        raise ValueError(
            "Input and Weight must have the same column dimension. "
            + f"Found {min_inputs.shape} and {min_weights.shape} shapes instead."
        )

    equalization_scale = torch.sqrt(
        (max_weights - min_weights) / (max_inputs - min_inputs)
    )
    # Replace all 'inf', 'nan', 0's with 1s to prevent errors
    equalization_scale[equalization_scale == 0.0] = 1
    equalization_scale = torch.nan_to_num(equalization_scale, nan=1, posinf=1, neginf=1)
    return equalization_scale

