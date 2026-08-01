
def test_safe_first_element_with_none():
    datetime_lst = [date.today() + timedelta(days=i) for i in range(10)]
    datetime_lst[0] = None
    actual = cbook._safe_first_finite(datetime_lst)
    assert actual is not None and actual == datetime_lst[1]

