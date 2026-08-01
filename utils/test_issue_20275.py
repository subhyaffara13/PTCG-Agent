
def test_issue_20275():
    # XXX We use complex expansions because complex exponentials are not
    # recognized by polys.domains
    A = DFT(3).as_explicit().expand(complex=True)
    eigenvects = A.eigenvects()
    assert eigenvects[0] == (
        -1, 1,
        [Matrix([[1 - sqrt(3)], [1], [1]])]
    )
    assert eigenvects[1] == (
        1, 1,
        [Matrix([[1 + sqrt(3)], [1], [1]])]
    )
    assert eigenvects[2] == (
        -I, 1,
        [Matrix([[0], [-1], [1]])]
    )

    A = DFT(4).as_explicit().expand(complex=True)
    eigenvects = A.eigenvects()
    assert eigenvects[0] == (
        -1, 1,
        [Matrix([[-1], [1], [1], [1]])]
    )
    assert eigenvects[1] == (
        1, 2,
        [Matrix([[1], [0], [1], [0]]), Matrix([[2], [1], [0], [1]])]
    )
    assert eigenvects[2] == (
        -I, 1,
        [Matrix([[0], [-1], [0], [1]])]
    )

    # XXX We skip test for some parts of eigenvectors which are very
    # complicated and fragile under expression tree changes
    A = DFT(5).as_explicit().expand(complex=True)
    eigenvects = A.eigenvects()
    assert eigenvects[0] == (
        -1, 1,
        [Matrix([[1 - sqrt(5)], [1], [1], [1], [1]])]
    )
    assert eigenvects[1] == (
        1, 2,
        [Matrix([[S(1)/2 + sqrt(5)/2], [0], [1], [1], [0]]),
         Matrix([[S(1)/2 + sqrt(5)/2], [1], [0], [0], [1]])]
    )

