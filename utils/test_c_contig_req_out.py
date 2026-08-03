import random

def test_c_contig_req_out(dtype):
    # GH 18704
    out = np.empty((2, 3), order="F", dtype=dtype)
    shape = [1, 2, 3]
    with pytest.raises(ValueError, match="Supplied output array"):
        random.standard_gamma(shape, out=out, dtype=dtype)
    with pytest.raises(ValueError, match="Supplied output array"):
        random.standard_gamma(shape, out=out, size=out.shape, dtype=dtype)

