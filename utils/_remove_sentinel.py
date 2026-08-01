
def _remove_sentinel(samples, paired, sentinel):
    "Remove sentinel values from paired or unpaired 1D samples"
    # could consolidate with `_remove_nans`, but it's not quite as simple as
    # passing `sentinel=np.nan` because `(np.nan == np.nan) is False`

    # potential optimization: don't copy arrays that don't contain sentinel
    if not paired:
        return [sample[sample != sentinel] for sample in samples]

    # for paired samples, we need to remove the whole pair when any part
    # has a nan
    sentinels = (samples[0] == sentinel)
    for sample in samples[1:]:
        sentinels = sentinels | (sample == sentinel)
    not_sentinels = ~sentinels
    return [sample[not_sentinels] for sample in samples]

