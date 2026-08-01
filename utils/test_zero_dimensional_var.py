
def test_zero_dimensional_var():
    io = BytesIO()
    with make_simple(io, 'w') as f:
        v = f.createVariable('zerodim', 'i2', [])
        # This is checking that .isrec returns a boolean - don't simplify it
        # to 'assert not ...'
        assert v.isrec is False, v.isrec
        f.flush()

