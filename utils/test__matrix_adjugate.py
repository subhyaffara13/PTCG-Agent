
def test_Matrix_adjugate(name, A, A_inv, den):
    A = A.to_Matrix()
    A_inv = A_inv.to_Matrix()
    assert A.adjugate() == A_inv
    for method in ["bareiss", "berkowitz", "bird", "laplace", "lu"]:
        assert A.adjugate(method=method) == A_inv

