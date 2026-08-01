
def test_contig_req_out(dist, order, dtype):
    # GH 18704
    out = np.empty((2, 3), dtype=dtype, order=order)
    variates = dist(out=out, dtype=dtype)
    assert variates is out
    variates = dist(out=out, dtype=dtype, size=out.shape)
    assert variates is out

