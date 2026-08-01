
def test_rcode_Integer():
    assert rcode(Integer(67)) == "67"
    assert rcode(Integer(-1)) == "-1"

