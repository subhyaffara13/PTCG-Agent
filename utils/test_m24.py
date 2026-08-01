
def test_M24():
    # TODO: Replace solve with solveset, as of now test fails for solveset
    solution = solve(1 - binomial(m, 2)*2**k, k)
    answer = log(2/(m*(m - 1)), 2)
    assert solution[0].expand() == answer.expand()

