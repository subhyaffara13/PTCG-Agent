
def _raw_fftnd(a, s=None, axes=None, function=fft, norm=None, out=None):
    a = asarray(a)
    s, axes = _cook_nd_args(a, s, axes)
    itl = list(range(len(axes)))
    itl.reverse()
    for ii in itl:
        a = function(a, n=s[ii], axis=axes[ii], norm=norm, out=out)
    return a

