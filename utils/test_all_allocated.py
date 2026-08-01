
def test_all_allocated():
    # When no output and no shape is given, `()` is used as shape.
    i = np.nditer([None], op_dtypes=["int64"])
    assert i.operands[0].shape == ()
    assert i.dtypes == (np.dtype("int64"),)

    i = np.nditer([None], op_dtypes=["int64"], itershape=(2, 3, 4))
    assert i.operands[0].shape == (2, 3, 4)

