
def test_maybe_infer_ndim_deprecated():
    # GH#40226
    msg = "maybe_infer_ndim is deprecated and will be removed in a future version."
    arr = np.arange(5)
    bp = pd._libs.internals.BlockPlacement([1])
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        internals.api.maybe_infer_ndim(arr, bp, 1)

