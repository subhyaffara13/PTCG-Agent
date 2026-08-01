
def test_days_of_week_value_error():
    msg = "days_of_week must be None or tuple."

    with pytest.raises(ValueError, match=msg):
        Holiday("World Blood Donor Day", month=6, day=14, days_of_week=[0, 1])

