
def test_sympy__physics__quantum__grover__OracleGateFunction():
    from sympy.physics.quantum.grover import OracleGateFunction
    @OracleGateFunction
    def f(qubit):
        return
    assert _test_args(f)

