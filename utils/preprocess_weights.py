
def preprocess_weights(obj: NDFrame, weights, axis: AxisInt) -> np.ndarray:
    """
    Process and validate the `weights` argument to `NDFrame.sample` and
    `.GroupBy.sample`.

    Returns `weights` as an ndarray[np.float64], validated except for normalizing
    weights (because that must be done groupwise in groupby sampling).
    """
    # If a series, align with frame
    if isinstance(weights, ABCSeries):
        weights = weights.reindex(obj.axes[axis])

    # Strings acceptable if a dataframe and axis = 0
    if isinstance(weights, str):
        if isinstance(obj, ABCDataFrame):
            if axis == 0:
                try:
                    weights = obj[weights]
                except KeyError as err:
                    raise KeyError(
                        "String passed to weights not a valid column"
                    ) from err
            else:
                raise ValueError(
                    "Strings can only be passed to "
                    "weights when sampling from rows on "
                    "a DataFrame"
                )
        else:
            raise ValueError(
                "Strings cannot be passed as weights when sampling from a Series."
            )

    if isinstance(obj, ABCSeries):
        func = obj._constructor
    else:
        func = obj._constructor_sliced

    weights = func(weights, dtype="float64")._values

    if len(weights) != obj.shape[axis]:
        raise ValueError("Weights and axis to be sampled must be of same length")

    if lib.has_infs(weights):
        raise ValueError("weight vector may not include `inf` values")

    if (weights < 0).any():
        raise ValueError("weight vector many not include negative values")

    missing = np.isnan(weights)
    if missing.any():
        # Don't modify weights in place
        weights = weights.copy()
        weights[missing] = 0
    return weights

