
def test_einsum_chunking_precision():
    """Most einsum operations are reductions and until NumPy 2.3 reductions
    never (or almost never?) used the `GROWINNER` mechanism to increase the
    inner loop size when no buffers are needed.
    Because einsum reductions work roughly:

        def inner(*inputs, out):
            accumulate = 0
            for vals in zip(*inputs):
                accumulate += prod(vals)
            out[0] += accumulate

    Calling the inner-loop more often actually improves accuracy slightly
    (same effect as pairwise summation but much less).
    Without adding pairwise summation to the inner-loop it seems best to just
    not use GROWINNER, a quick tests suggest that is maybe 1% slowdown for
    the simplest `einsum("i,i->i", x, x)` case.

    (It is not clear that we should guarantee precision to this extend.)
    """
    num = 1_000_000
    value = 1. + np.finfo(np.float64).eps * 8196
    res = np.einsum("i->", np.broadcast_to(np.array(value), num)) / num

    # At with GROWINNER 11 decimals succeed (larger will be less)
    assert_almost_equal(res, value, decimal=15)

