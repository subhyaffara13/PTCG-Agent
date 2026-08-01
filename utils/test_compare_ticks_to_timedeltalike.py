
def test_compare_ticks_to_timedeltalike(cls):
    off = cls(19)

    td = off._as_pd_timedelta

    others = [td, td.to_timedelta64()]
    if cls is not Nano:
        others.append(td.to_pytimedelta())

    for other in others:
        assert off == other
        assert not off != other
        assert not off < other
        assert not off > other
        assert off <= other
        assert off >= other

