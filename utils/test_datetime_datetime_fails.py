
def test_datetime_datetime_fails():
    from datetime import datetime

    start = datetime(2017, 1, 1, 0, 0, 0)
    dt_delta = datetime(1970, 1, 5)  # Will be 5 days if units are done wrong.

    with pytest.raises(TypeError):
        mpatches.Rectangle((start, 0), dt_delta, 1)

    with pytest.raises(TypeError):
        mpatches.Rectangle((0, start), 1, dt_delta)

