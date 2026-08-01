
def test_gate_sort():
    """Test gate_sort."""
    for g in (X, Y, Z, H, S, T):
        assert gate_sort(g(2)*g(1)*g(0)) == g(0)*g(1)*g(2)
    e = gate_sort(X(1)*H(0)**2*CNOT(0, 1)*X(1)*X(0))
    assert e == H(0)**2*CNOT(0, 1)*X(0)*X(1)**2
    assert gate_sort(Z(0)*X(0)) == -X(0)*Z(0)
    assert gate_sort(Z(0)*X(0)**2) == X(0)**2*Z(0)
    assert gate_sort(Y(0)*H(0)) == -H(0)*Y(0)
    assert gate_sort(Y(0)*X(0)) == -X(0)*Y(0)
    assert gate_sort(Z(0)*Y(0)) == -Y(0)*Z(0)
    assert gate_sort(T(0)*S(0)) == S(0)*T(0)
    assert gate_sort(Z(0)*S(0)) == S(0)*Z(0)
    assert gate_sort(Z(0)*T(0)) == T(0)*Z(0)
    assert gate_sort(Z(0)*CNOT(0, 1)) == CNOT(0, 1)*Z(0)
    assert gate_sort(S(0)*CNOT(0, 1)) == CNOT(0, 1)*S(0)
    assert gate_sort(T(0)*CNOT(0, 1)) == CNOT(0, 1)*T(0)
    assert gate_sort(X(1)*CNOT(0, 1)) == CNOT(0, 1)*X(1)

