
def test_adjoint_with_operator():
    # Regression test for issue 25130: adjoint() should propagate to operators
    import sympy.physics.quantum
    a = sympy.physics.quantum.operator.Operator('a')
    a_dag = sympy.physics.quantum.Dagger(a)
    dat = [[0, I * a], [0, a_dag]]
    ans = Matrix([[0, 0], [-I * a_dag, a]])
    for cls in classes:
        assert ans == cls(dat).adjoint()

