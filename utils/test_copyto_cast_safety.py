
def test_copyto_cast_safety():
    with pytest.raises(TypeError):
        np.copyto(np.arange(3), 3., casting="safe")

    # Can put integer and float scalars safely (and equiv):
    np.copyto(np.arange(3), 3, casting="equiv")
    np.copyto(np.arange(3.), 3., casting="equiv")
    # And also with less precision safely:
    np.copyto(np.arange(3, dtype="uint8"), 3, casting="safe")
    np.copyto(np.arange(3., dtype="float32"), 3., casting="safe")

    # But not equiv:
    with pytest.raises(TypeError):
        np.copyto(np.arange(3, dtype="uint8"), 3, casting="equiv")

    with pytest.raises(TypeError):
        np.copyto(np.arange(3., dtype="float32"), 3., casting="equiv")

    # As a special thing, object is equiv currently:
    np.copyto(np.arange(3, dtype=object), 3, casting="equiv")

    # The following raises an overflow error/gives a warning but not
    # type error (due to casting), though:
    with pytest.raises(OverflowError):
        np.copyto(np.arange(3), 2**80, casting="safe")

    with pytest.warns(RuntimeWarning):
        np.copyto(np.arange(3, dtype=np.float32), 2e300, casting="safe")

