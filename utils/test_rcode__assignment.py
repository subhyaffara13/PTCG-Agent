
def test_rcode_Assignment():
    assert rcode(Assignment(x, y + z)) == 'x = y + z;'
    assert rcode(aug_assign(x, '+', y + z)) == 'x += y + z;'

