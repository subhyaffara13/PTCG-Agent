
def _alexandergovern_input_validation(samples, nan_policy, axis, xp):
    if len(samples) < 2:
        raise TypeError(f"2 or more inputs required, got {len(samples)}")

    for sample in samples:
        if sample.shape[axis] <= 1:
            raise ValueError("Input sample size must be greater than one.")

    samples = [xp.moveaxis(sample, axis, -1) for sample in samples]

    return samples

