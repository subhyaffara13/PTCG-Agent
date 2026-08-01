
def test_internal_overlap_diophantine():
    def check(A, U, exists=None):
        X = solve_diophantine(A, U, 0, require_ub_nontrivial=1)

        if exists is None:
            exists = (X is not None)

        if X is not None:
            sum_ax = sum(a * x for a, x in zip(A, X))
            sum_au_half = sum(a * u // 2 for a, u in zip(A, U))
            assert_(sum_ax == sum_au_half)
            assert_(all(0 <= x <= u for x, u in zip(X, U)))
            assert_(any(x != u // 2 for x, u in zip(X, U)))

        if exists:
            assert_(X is not None, repr(X))
        else:
            assert_(X is None, repr(X))

    # Smoke tests
    check((3, 2), (2 * 2, 3 * 2), exists=True)
    check((3 * 2, 2), (15 * 2, (3 - 1) * 2), exists=False)

