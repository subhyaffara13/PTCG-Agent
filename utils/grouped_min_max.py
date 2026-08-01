
def grouped_min_max(
    values: np.ndarray,
    result_dtype: np.dtype,
    labels: npt.NDArray[np.intp],
    ngroups: int,
    min_periods: int,
    is_max: bool,
    skipna: bool = True,
) -> tuple[np.ndarray, list[int]]:
    N = len(labels)
    nobs = np.zeros(ngroups, dtype=np.int64)
    na_pos = []
    output = np.empty(ngroups, dtype=result_dtype)

    for i in range(N):
        lab = labels[i]
        val = values[i]
        if lab < 0 or (not skipna and nobs[lab] >= 1 and np.isnan(output[lab])):
            continue

        if values.dtype.kind == "i" or not np.isnan(val):
            nobs[lab] += 1
        else:
            if not skipna:
                # If skipna is False and we encounter a NaN,
                # both min and max of the group will be NaN
                output[lab] = np.nan
            continue

        if nobs[lab] == 1:
            # First element in group, set output equal to this
            output[lab] = val
            continue

        if is_max:
            if val > output[lab]:
                output[lab] = val
        elif val < output[lab]:
            output[lab] = val

    # Set labels that don't satisfy min_periods as np.nan
    for lab, count in enumerate(nobs):
        if count < min_periods:
            na_pos.append(lab)

    return output, na_pos

