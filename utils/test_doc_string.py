
def test_doc_string(m, doc):
    assert (
        doc(m.copy_tensor) == "copy_tensor() -> numpy.ndarray[numpy.float64[?, ?, ?]]"
    )
    assert (
        doc(m.copy_fixed_tensor)
        == "copy_fixed_tensor() -> numpy.ndarray[numpy.float64[3, 5, 2]]"
    )
    assert (
        doc(m.reference_const_tensor)
        == "reference_const_tensor() -> numpy.ndarray[numpy.float64[?, ?, ?]]"
    )

    order_flag = f"flags.{m.needed_options.lower()}_contiguous"
    assert doc(m.round_trip_view_tensor) == (
        f"round_trip_view_tensor(arg0: numpy.ndarray[numpy.float64[?, ?, ?], flags.writeable, {order_flag}])"
        f" -> numpy.ndarray[numpy.float64[?, ?, ?], flags.writeable, {order_flag}]"
    )
    assert doc(m.round_trip_const_view_tensor) == (
        f"round_trip_const_view_tensor(arg0: numpy.ndarray[numpy.float64[?, ?, ?], {order_flag}])"
        " -> numpy.ndarray[numpy.float64[?, ?, ?]]"
    )


def test_doc_string():
    df = DataFrame({"B": [0, 1, 2, np.nan, 4]})
    df
    df.ewm(com=0.5).mean()


def test_doc_string():
    df = DataFrame({"B": [0, 1, 2, np.nan, 4]})
    df
    df.expanding(2).sum()


def test_doc_string():
    df = DataFrame({"B": [0, 1, 2, np.nan, 4]})
    df
    df.rolling(2).sum()
    df.rolling(2, min_periods=1).sum()

