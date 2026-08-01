
def test_nonsubclassable(cls):
    with pytest.raises(Exception, match="(?i)subclassing"):

        class Boom(cls):  # pragma: no cover
            pass

