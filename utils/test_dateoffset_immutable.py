
def test_dateoffset_immutable(attribute):
    offset = DateOffset(**{attribute: 0})
    msg = "DateOffset objects are immutable"
    with pytest.raises(AttributeError, match=msg):
        setattr(offset, attribute, 5)

