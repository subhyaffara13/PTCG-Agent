
def test_jn_zeros():
    assert eq(jn_zeros(0, 4), [3.141592, 6.283185, 9.424777, 12.566370])
    assert eq(jn_zeros(1, 4), [4.493409, 7.725251, 10.904121, 14.066193])
    assert eq(jn_zeros(2, 4), [5.763459, 9.095011, 12.322940, 15.514603])
    assert eq(jn_zeros(3, 4), [6.987932, 10.417118, 13.698023, 16.923621])
    assert eq(jn_zeros(4, 4), [8.182561, 11.704907, 15.039664, 18.301255])


def test_jn_zeros():
    assert eq(jn_zeros(0, 4, method="scipy"),
            [3.141592, 6.283185, 9.424777, 12.566370])
    assert eq(jn_zeros(1, 4, method="scipy"),
            [4.493409, 7.725251, 10.904121, 14.066193])
    assert eq(jn_zeros(2, 4, method="scipy"),
            [5.763459, 9.095011, 12.322940, 15.514603])
    assert eq(jn_zeros(3, 4, method="scipy"),
            [6.987932, 10.417118, 13.698023, 16.923621])
    assert eq(jn_zeros(4, 4, method="scipy"),
            [8.182561, 11.704907, 15.039664, 18.301255])

