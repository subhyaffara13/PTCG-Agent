
def test_embedded_null_comparisons(op, pyop):
    lhs = ["a\0b", "a\0b", "a\0c", "\0b", "long\0b"]
    rhs = ["a\0c", "a\0b", "a\0b", "\0a", "long\0c"]

    expected = [pyop(left, right) for left, right in zip(lhs, rhs)]
    result = op(np.array(lhs, dtype="T"), np.array(rhs, dtype="T"))

    assert result.tolist() == expected

