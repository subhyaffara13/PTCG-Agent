
def test_find_simple_recurrence_vector():
    assert find_simple_recurrence_vector(
            [fibonacci(k) for k in range(12)]) == [1, -1, -1]

