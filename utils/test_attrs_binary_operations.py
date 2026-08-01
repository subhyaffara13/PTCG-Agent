
def test_attrs_binary_operations(all_binary_operators, left, right):
    # GH 51607
    attrs = {"a": 1}
    left = left([1])
    left.attrs = attrs
    right = right([2])
    assert all_binary_operators(left, right).attrs == attrs
    assert all_binary_operators(right, left).attrs == attrs

