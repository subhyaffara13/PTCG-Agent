
def test_issue_8496():
    n = Symbol("n")
    k = Symbol("k")

    raises(TypeError, lambda: catalan(n, k))

