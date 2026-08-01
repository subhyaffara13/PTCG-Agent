
def _jackknife_resample(sample, batch=None, *, xp):
    """Jackknife resample the sample. Only one-sample stats for now."""
    n = sample.shape[-1]
    batch_nominal = batch or n

    for k in range(0, n, batch_nominal):
        # col_start:col_end are the observations to remove
        batch_actual = min(batch_nominal, n-k)

        # jackknife - each row leaves out one observation
        j = np.ones((batch_actual, n), dtype=bool)
        np.fill_diagonal(j[:, k:k+batch_actual], False)
        i = np.arange(n)
        i = np.broadcast_to(i, (batch_actual, n))
        i = i[j].reshape((batch_actual, n-1))

        i = xp.asarray(i, device=xp_device(sample))
        yield _get_from_last_axis(sample, i, xp=xp)

