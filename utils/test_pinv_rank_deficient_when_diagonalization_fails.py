
def test_pinv_rank_deficient_when_diagonalization_fails():
    # Test the four properties of the pseudoinverse for matrices when
    # diagonalization of A.H*A fails.
    As = [
        Matrix([
            [61, 89, 55, 20, 71, 0],
            [62, 96, 85, 85, 16, 0],
            [69, 56, 17,  4, 54, 0],
            [10, 54, 91, 41, 71, 0],
            [ 7, 30, 10, 48, 90, 0],
            [0, 0, 0, 0, 0, 0]])
    ]
    for A in As:
        A_pinv = A.pinv(method="ED")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert AAp.H == AAp

        # Here ApA.H and ApA are equivalent expressions but they are very
        # complicated expressions involving RootOfs. Using simplify would be
        # too slow and so would evalf so we substitute approximate values for
        # the RootOfs and then evalf which is less accurate but good enough to
        # confirm that these two matrices are equivalent.
        #
        # assert ApA.H == ApA  # <--- would fail (structural equality)
        # assert simplify(ApA.H - ApA).is_zero_matrix  # <--- too slow
        # (ApA.H - ApA).evalf()  # <--- too slow

        def allclose(M1, M2):
            rootofs = M1.atoms(RootOf)
            rootofs_approx = {r: r.evalf() for r in rootofs}
            diff_approx = (M1 - M2).xreplace(rootofs_approx).evalf()
            return all(abs(e) < 1e-10 for e in diff_approx)

        assert allclose(ApA.H, ApA)


def test_pinv_rank_deficient_when_diagonalization_fails():
    # Test the four properties of the pseudoinverse for matrices when
    # diagonalization of A.H*A fails.
    As = [
        Matrix([
            [61, 89, 55, 20, 71, 0],
            [62, 96, 85, 85, 16, 0],
            [69, 56, 17,  4, 54, 0],
            [10, 54, 91, 41, 71, 0],
            [ 7, 30, 10, 48, 90, 0],
            [0, 0, 0, 0, 0, 0]])
    ]
    for A in As:
        A_pinv = A.pinv(method="ED")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert AAp.H == AAp

        # Here ApA.H and ApA are equivalent expressions but they are very
        # complicated expressions involving RootOfs. Using simplify would be
        # too slow and so would evalf so we substitute approximate values for
        # the RootOfs and then evalf which is less accurate but good enough to
        # confirm that these two matrices are equivalent.
        #
        # assert ApA.H == ApA  # <--- would fail (structural equality)
        # assert simplify(ApA.H - ApA).is_zero_matrix  # <--- too slow
        # (ApA.H - ApA).evalf()  # <--- too slow

        def allclose(M1, M2):
            rootofs = M1.atoms(RootOf)
            rootofs_approx = {r: r.evalf() for r in rootofs}
            diff_approx = (M1 - M2).xreplace(rootofs_approx).evalf()
            return all(abs(e) < 1e-10 for e in diff_approx)

        assert allclose(ApA.H, ApA)

