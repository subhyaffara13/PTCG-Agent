
def _upsample_nearest_exact1d(x, output_size, scales: float | None = None):
    return upsample_nearestnd(x, output_size, (scales,), n=1, exact=True)

