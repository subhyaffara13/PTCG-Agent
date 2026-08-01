
def test_axline_minmax(fv, fh, args):
    bad_lim = matplotlib.dates.num2date(1)
    # Check vertical functions
    with pytest.raises(ValueError, match='ymin must be a single scalar value'):
        fv(*args, ymin=bad_lim, ymax=1)
    with pytest.raises(ValueError, match='ymax must be a single scalar value'):
        fv(*args, ymin=1, ymax=bad_lim)
    # Check horizontal functions
    with pytest.raises(ValueError, match='xmin must be a single scalar value'):
        fh(*args, xmin=bad_lim, xmax=1)
    with pytest.raises(ValueError, match='xmax must be a single scalar value'):
        fh(*args, xmin=1, xmax=bad_lim)

