
def test_memmap_takes_fast_route(tmpdir):
    # We want memory mapped arrays to take the fast route through nanmax,
    # which avoids creating a mask by using fmax.reduce (see gh-28721). So we
    # check that on bad input, the error is from fmax (rather than maximum).
    a = np.arange(10., dtype=float)
    with open(tmpdir.join("data.bin"), "w+b") as fh:
        fh.write(a.tobytes())
        mm = np.memmap(fh, dtype=a.dtype, shape=a.shape)
        with pytest.raises(ValueError, match="reduction operation fmax"):
            np.nanmax(mm, out=np.zeros(2))
        # For completeness, same for nanmin.
        with pytest.raises(ValueError, match="reduction operation fmin"):
            np.nanmin(mm, out=np.zeros(2))

