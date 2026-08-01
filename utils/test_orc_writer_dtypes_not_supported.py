
def test_orc_writer_dtypes_not_supported(orc_writer_dtypes_not_supported):
    # GH44554
    # PyArrow gained ORC write support with the current argument order
    pytest.importorskip("pyarrow")

    df = pd.DataFrame({"unimpl": orc_writer_dtypes_not_supported})
    msg = "The dtype of one or more columns is not supported yet."
    with pytest.raises(NotImplementedError, match=msg):
        df.to_orc()

