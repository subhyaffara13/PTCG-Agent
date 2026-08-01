
def _remove_nans(samples, paired, xp=None):
    "Remove nans from paired or unpaired 1D samples"
    # potential optimization: don't copy arrays that don't contain nans
    xp = array_namespace(*samples)
    if not paired:
        return [sample[~xp.isnan(sample)] for sample in samples]

    # for paired samples, we need to remove the whole pair when any part
    # has a nan
    nans = xp.isnan(samples[0])
    for sample in samples[1:]:
        nans = nans | xp.isnan(sample)
    not_nans = ~nans
    return [sample[not_nans] for sample in samples]

