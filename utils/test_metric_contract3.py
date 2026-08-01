
def test_metric_contract3():
    D = Symbol('D')
    Spinor = TensorIndexType('Spinor', dim=D, metric_symmetry=-1, dummy_name='S')
    a0, a1, a2, a3, a4 = tensor_indices('a0:5', Spinor)
    C = Spinor.metric
    chi, psi = tensor_heads('chi,psi', [Spinor], TensorSymmetry.no_symmetry(1), 1)
    B = TensorHead('B', [Spinor]*2, TensorSymmetry.no_symmetry(2))

    t = C(a0,-a0)
    t1 = t.contract_metric(C)
    assert t1.equals(-D)

    t = C(-a0,a0)
    t1 = t.contract_metric(C)
    assert t1.equals(D)

    t = C(a0,a1)*C(-a0,-a1)
    t1 = t.contract_metric(C)
    assert t1.equals(D)

    t = C(a1,a0)*C(-a0,-a1)
    t1 = t.contract_metric(C)
    assert t1.equals(-D)

    t = C(-a0,a1)*C(a0,-a1)
    t1 = t.contract_metric(C)
    assert t1.equals(-D)

    t = C(a1,-a0)*C(a0,-a1)
    t1 = t.contract_metric(C)
    assert t1.equals(D)

    t = C(a0,a1)*B(-a1,-a0)
    t1 = t.contract_metric(C)
    t1 = t1.canon_bp()
    assert _is_equal(t1, B(a0,-a0))

    t = C(a1,a0)*B(-a1,-a0)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -B(a0,-a0))

    t = C(a0,-a1)*B(a1,-a0)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -B(a0,-a0))

    t = C(-a0,a1)*B(-a1,a0)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -B(a0,-a0))

    t = C(-a0,-a1)*B(a1,a0)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, B(a0,-a0))

    t = C(-a1, a0)*B(a1,-a0)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, B(a0,-a0))

    t = C(a0,a1)*psi(-a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, psi(a0))

    t = C(a1,a0)*psi(-a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -psi(a0))

    t = C(a0,a1)*chi(-a0)*psi(-a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -chi(a1)*psi(-a1))

    t = C(a1,a0)*chi(-a0)*psi(-a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, chi(a1)*psi(-a1))

    t = C(-a1,a0)*chi(-a0)*psi(a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, chi(-a1)*psi(a1))

    t = C(a0,-a1)*chi(-a0)*psi(a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -chi(-a1)*psi(a1))

    t = C(-a0,-a1)*chi(a0)*psi(a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, chi(-a1)*psi(a1))

    t = C(-a1,-a0)*chi(a0)*psi(a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -chi(-a1)*psi(a1))

    t = C(-a1,-a0)*B(a0,a2)*psi(a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, -B(-a1,a2)*psi(a1))

    t = C(a1,a0)*B(-a2,-a0)*psi(-a1)
    t1 = t.contract_metric(C)
    assert _is_equal(t1, B(-a2,a1)*psi(-a1))

