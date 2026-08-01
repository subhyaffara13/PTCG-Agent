
def test_issue24158_ket_times_op():
    P = BosonFockKet(0) * BosonOp("a") # undefined term
    # Does lhs._apply_operator_BosonOp(rhs) still evaluate ket*op as op*ket?
    assert qapply(P) == P   # qapply(P) -> BosonOp("a")*BosonFockKet(0) = 0 before fix
    P = Qubit(1) * XGate(0) # undefined term
    # Does rhs._apply_operator_Qubit(lhs) still evaluate ket*op as op*ket?
    assert qapply(P) == P   # qapply(P) -> Qubit(0) before fix
    P1 = Mul(QubitBra(0), Mul(QubitBra(0), Qubit(0)), XGate(0)) # legal expr <0| * (<1|*|1>) * X
    assert qapply(P1) == QubitBra(0) * XGate(0)     # qapply(P1) -> 0 before fix
    P1 = qapply(P1, dagger = True)  # unsatisfactorily -> <0|*X(0), expect <1| since dagger=True
    assert qapply(P1, dagger = True) == QubitBra(1) # qapply(P1, dagger=True) -> 0 before fix
    P2 = QubitBra(0) * (QubitBra(0) * Qubit(0)) * XGate(0) # 'forgot' to set brackets
    P2 = qapply(P2, dagger = True) # unsatisfactorily -> <0|*X(0), expect <1| since dagger=True
    assert P2 == QubitBra(1) # qapply(P1) -> 0 before fix
    # Pull Request 24237: IdentityOperator from the right without dagger=True option
    with warns_deprecated_sympy():
        assert qapply(QubitBra(1)*IdentityOperator()) == QubitBra(1)
        assert qapply(IdentityGate(0)*(Qubit(0) + Qubit(1))) == Qubit(0) + Qubit(1)

