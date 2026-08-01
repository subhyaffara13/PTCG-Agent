
def test_number_protocol():
    for a, b in [(1, 1), (3, 5)]:
        li = [
            a == b,
            a != b,
            a < b,
            a <= b,
            a > b,
            a >= b,
            a + b,
            a - b,
            a * b,
            a / b,
            a | b,
            a & b,
            a ^ b,
            a >> b,
            a << b,
        ]
        assert m.test_number_protocol(a, b) == li

