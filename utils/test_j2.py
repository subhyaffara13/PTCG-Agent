
def test_J2():
    assert diff(elliptic_e(x, y**2), y) == (elliptic_e(x, y**2) - elliptic_f(x, y**2))/y


def test_j2():
    assert Commutator(J2, Jz).doit() == 0
    assert J2.matrix_element(1, 1, 1, 1) == 2*hbar**2
    # Normal operators, normal states
    # Numerical
    assert qapply(J2*JxKet(1, 1)) == 2*hbar**2*JxKet(1, 1)
    assert qapply(J2*JyKet(1, 1)) == 2*hbar**2*JyKet(1, 1)
    assert qapply(J2*JzKet(1, 1)) == 2*hbar**2*JzKet(1, 1)
    # Symbolic
    assert qapply(J2*JxKet(j, m)) == \
        hbar**2*j**2*JxKet(j, m) + hbar**2*j*JxKet(j, m)
    assert qapply(J2*JyKet(j, m)) == \
        hbar**2*j**2*JyKet(j, m) + hbar**2*j*JyKet(j, m)
    assert qapply(J2*JzKet(j, m)) == \
        hbar**2*j**2*JzKet(j, m) + hbar**2*j*JzKet(j, m)
    # Normal operators, coupled states
    # Numerical
    assert qapply(J2*JxKetCoupled(1, 1, (1, 1))) == \
        2*hbar**2*JxKetCoupled(1, 1, (1, 1))
    assert qapply(J2*JyKetCoupled(1, 1, (1, 1))) == \
        2*hbar**2*JyKetCoupled(1, 1, (1, 1))
    assert qapply(J2*JzKetCoupled(1, 1, (1, 1))) == \
        2*hbar**2*JzKetCoupled(1, 1, (1, 1))
    # Symbolic
    assert qapply(J2*JxKetCoupled(j, m, (j1, j2))) == \
        hbar**2*j**2*JxKetCoupled(j, m, (j1, j2)) + \
        hbar**2*j*JxKetCoupled(j, m, (j1, j2))
    assert qapply(J2*JyKetCoupled(j, m, (j1, j2))) == \
        hbar**2*j**2*JyKetCoupled(j, m, (j1, j2)) + \
        hbar**2*j*JyKetCoupled(j, m, (j1, j2))
    assert qapply(J2*JzKetCoupled(j, m, (j1, j2))) == \
        hbar**2*j**2*JzKetCoupled(j, m, (j1, j2)) + \
        hbar**2*j*JzKetCoupled(j, m, (j1, j2))
    # Uncoupled operators, uncoupled states
    # Numerical
    assert qapply(TensorProduct(J2, 1)*TensorProduct(JxKet(1, 1), JxKet(1, -1))) == \
        2*hbar**2*TensorProduct(JxKet(1, 1), JxKet(1, -1))
    assert qapply(TensorProduct(1, J2)*TensorProduct(JxKet(1, 1), JxKet(1, -1))) == \
        2*hbar**2*TensorProduct(JxKet(1, 1), JxKet(1, -1))
    assert qapply(TensorProduct(J2, 1)*TensorProduct(JyKet(1, 1), JyKet(1, -1))) == \
        2*hbar**2*TensorProduct(JyKet(1, 1), JyKet(1, -1))
    assert qapply(TensorProduct(1, J2)*TensorProduct(JyKet(1, 1), JyKet(1, -1))) == \
        2*hbar**2*TensorProduct(JyKet(1, 1), JyKet(1, -1))
    assert qapply(TensorProduct(J2, 1)*TensorProduct(JzKet(1, 1), JzKet(1, -1))) == \
        2*hbar**2*TensorProduct(JzKet(1, 1), JzKet(1, -1))
    assert qapply(TensorProduct(1, J2)*TensorProduct(JzKet(1, 1), JzKet(1, -1))) == \
        2*hbar**2*TensorProduct(JzKet(1, 1), JzKet(1, -1))
    # Symbolic
    e1 = qapply(TensorProduct(J2, 1)*TensorProduct(JxKet(j1, m1), JxKet(j2, m2)))
    e2 = hbar**2*j1**2*TensorProduct(JxKet(j1, m1), JxKet(j2, m2)) + \
        hbar**2*j1*TensorProduct(JxKet(j1, m1), JxKet(j2, m2))
    assert_simplify_expand(e1, e2)
    e1 = qapply(TensorProduct(1, J2)*TensorProduct(JxKet(j1, m1), JxKet(j2, m2)))
    e2 = hbar**2*j2**2*TensorProduct(JxKet(j1, m1), JxKet(j2, m2)) + \
        hbar**2*j2*TensorProduct(JxKet(j1, m1), JxKet(j2, m2))
    assert_simplify_expand(e1, e2)
    e1 = qapply(TensorProduct(J2, 1)*TensorProduct(JyKet(j1, m1), JyKet(j2, m2)))
    e2 = hbar**2*j1**2*TensorProduct(JyKet(j1, m1), JyKet(j2, m2)) + \
        hbar**2*j1*TensorProduct(JyKet(j1, m1), JyKet(j2, m2))
    assert_simplify_expand(e1, e2)
    e1 = qapply(TensorProduct(1, J2)*TensorProduct(JyKet(j1, m1), JyKet(j2, m2)))
    e2 = hbar**2*j2**2*TensorProduct(JyKet(j1, m1), JyKet(j2, m2)) + \
        hbar**2*j2*TensorProduct(JyKet(j1, m1), JyKet(j2, m2))
    assert_simplify_expand(e1, e2)
    e1 = qapply(TensorProduct(J2, 1)*TensorProduct(JzKet(j1, m1), JzKet(j2, m2)))
    e2 = hbar**2*j1**2*TensorProduct(JzKet(j1, m1), JzKet(j2, m2)) + \
        hbar**2*j1*TensorProduct(JzKet(j1, m1), JzKet(j2, m2))
    assert_simplify_expand(e1, e2)
    e1 = qapply(TensorProduct(1, J2)*TensorProduct(JzKet(j1, m1), JzKet(j2, m2)))
    e2 = hbar**2*j2**2*TensorProduct(JzKet(j1, m1), JzKet(j2, m2)) + \
        hbar**2*j2*TensorProduct(JzKet(j1, m1), JzKet(j2, m2))
    assert_simplify_expand(e1, e2)

