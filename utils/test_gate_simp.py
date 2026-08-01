
def test_gate_simp():
    """Test gate_simp."""
    e = H(0)*X(1)*H(0)**2*CNOT(0, 1)*X(1)**3*X(0)*Z(3)**2*S(4)**3
    assert gate_simp(e) == H(0)*CNOT(0, 1)*S(4)*X(0)*Z(4)
    assert gate_simp(X(0)*X(0)) == 1
    assert gate_simp(Y(0)*Y(0)) == 1
    assert gate_simp(Z(0)*Z(0)) == 1
    assert gate_simp(H(0)*H(0)) == 1
    assert gate_simp(T(0)*T(0)) == S(0)
    assert gate_simp(S(0)*S(0)) == Z(0)
    assert gate_simp(Integer(1)) == Integer(1)
    assert gate_simp(X(0)**2 + Y(0)**2) == Integer(2)

