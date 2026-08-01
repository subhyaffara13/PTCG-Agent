
def test_byteswapping_and_unaligned(dtype, value, swap):
    # Try to create "interesting" values within the valid unicode range:
    dtype = np.dtype(dtype)
    data = [f"x,{value}\n"]
    if swap:
        dtype = dtype.newbyteorder()
    full_dt = np.dtype([("a", "S1"), ("b", dtype)], align=False)
    # The above ensures that the interesting "b" field is unaligned:
    assert full_dt.fields["b"][1] == 1
    res = np.loadtxt(data, dtype=full_dt, delimiter=",",
                     max_rows=1)  # max-rows prevents over-allocation
    assert res["b"] == dtype.type(value)

