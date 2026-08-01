
def test_tick_division(cls):
    off = cls(10)

    assert off / cls(5) == 2
    assert off / 2 == cls(5)
    assert off / 2.0 == cls(5)

    assert off / off._as_pd_timedelta == 1
    assert off / off._as_pd_timedelta.to_timedelta64() == 1

    assert off / Nano(1) == off._as_pd_timedelta / Nano(1)._as_pd_timedelta

    if cls is not Nano:
        # A case where we end up with a smaller class
        result = off / 1000
        assert isinstance(result, offsets.Tick)
        assert not isinstance(result, cls)
        assert result._as_pd_timedelta == off._as_pd_timedelta / 1000

    if cls._nanos_inc < Timedelta(seconds=1)._value:
        # Case where we end up with a bigger class
        result = off / 0.001
        assert isinstance(result, offsets.Tick)
        assert not isinstance(result, cls)
        assert result._as_pd_timedelta == off._as_pd_timedelta / 0.001

