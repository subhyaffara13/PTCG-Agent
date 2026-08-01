
def test_oob_creation(sctype, create):
    iinfo = np.iinfo(sctype)

    with pytest.raises(OverflowError):
        create(sctype, iinfo.min - 1)

    with pytest.raises(OverflowError):
        create(sctype, iinfo.max + 1)

    with pytest.raises(OverflowError):
        create(sctype, str(iinfo.min - 1))

    with pytest.raises(OverflowError):
        create(sctype, str(iinfo.max + 1))

    assert create(sctype, iinfo.min) == iinfo.min
    assert create(sctype, iinfo.max) == iinfo.max

