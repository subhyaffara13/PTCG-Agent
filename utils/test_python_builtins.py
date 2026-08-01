
def test_python_builtins():
    """Test if python builtins like sum() can be used as callbacks"""
    assert m.test_sum_builtin(sum, [1, 2, 3]) == 6
    assert m.test_sum_builtin(sum, []) == 0

