
def _execute(duccfft_func, x, type, s, axes, norm, 
             overwrite_x, workers, orthogonalize):
    xp = array_namespace(x)
    x = np.asarray(x)
    y = duccfft_func(x, type, s, axes, norm,
                       overwrite_x=overwrite_x, workers=workers,
                       orthogonalize=orthogonalize)
    return xp.asarray(y)

