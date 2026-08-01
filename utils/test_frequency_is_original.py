
def test_frequency_is_original(num_cols, engine, request):
    # GH 22150
    if engine == "numba":
        mark = pytest.mark.xfail(reason="numba engine only supports numeric indices")
        request.node.add_marker(mark)
    index = pd.DatetimeIndex(["1950-06-30", "1952-10-24", "1953-05-29"])
    original = index.copy()
    df = DataFrame(1, index=index, columns=range(num_cols))
    df.apply(lambda x: x, engine=engine)
    assert index.freq == original.freq

