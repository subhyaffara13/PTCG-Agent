
def paired_non_broadcastable_cases():
    for case in axis_nan_policy_cases:
        hypotest, args, kwds, n_samples, n_outputs, paired, unpacker = case
        if n_samples == 1:  # broadcasting only needed with >1 sample
            continue
        yield case

