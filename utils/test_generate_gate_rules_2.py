
def test_generate_gate_rules_2():
    # Test with Muls
    (x, y, z, h) = create_gate_sequence()
    ph = PhaseGate(0)
    cgate_t = CGate(0, TGate(1))

    # Note: 1 (type int) is not the same as 1 (type One)
    expected = {(x, Integer(1))}
    assert generate_gate_rules((x,), return_as_muls=True) == expected

    expected = {(Integer(1), Integer(1))}
    assert generate_gate_rules(x*x, return_as_muls=True) == expected

    expected = {((), ())}
    assert generate_gate_rules(x*x, return_as_muls=False) == expected

    gate_rules = {(x*y*x, Integer(1)),
                      (y, Integer(1)),
                      (y*x, x),
                      (x*y, x)}
    assert generate_gate_rules(x*y*x, return_as_muls=True) == gate_rules

    gate_rules = {(x*y*z, Integer(1)),
                      (y*z*x, Integer(1)),
                      (z*x*y, Integer(1)),
                      (Integer(1), x*z*y),
                      (Integer(1), y*x*z),
                      (Integer(1), z*y*x),
                      (x, z*y),
                      (y*z, x),
                      (y, x*z),
                      (z*x, y),
                      (z, y*x),
                      (x*y, z)}
    actual = generate_gate_rules(x*y*z, return_as_muls=True)
    assert actual == gate_rules

    gate_rules = {(Integer(1), h*z*y*x),
                      (Integer(1), x*h*z*y),
                      (Integer(1), y*x*h*z),
                      (Integer(1), z*y*x*h),
                      (h, z*y*x), (x, h*z*y),
                      (y, x*h*z), (z, y*x*h),
                      (h*x, z*y), (z*h, y*x),
                      (x*y, h*z), (y*z, x*h),
                      (h*x*y, z), (x*y*z, h),
                      (y*z*h, x), (z*h*x, y),
                      (h*x*y*z, Integer(1)),
                      (x*y*z*h, Integer(1)),
                      (y*z*h*x, Integer(1)),
                      (z*h*x*y, Integer(1))}
    actual = generate_gate_rules(x*y*z*h, return_as_muls=True)
    assert actual == gate_rules

    gate_rules = {(Integer(1), cgate_t**(-1)*ph**(-1)*x),
                      (Integer(1), ph**(-1)*x*cgate_t**(-1)),
                      (Integer(1), x*cgate_t**(-1)*ph**(-1)),
                      (cgate_t, ph**(-1)*x),
                      (ph, x*cgate_t**(-1)),
                      (x, cgate_t**(-1)*ph**(-1)),
                      (cgate_t*x, ph**(-1)),
                      (ph*cgate_t, x),
                      (x*ph, cgate_t**(-1)),
                      (cgate_t*x*ph, Integer(1)),
                      (ph*cgate_t*x, Integer(1)),
                      (x*ph*cgate_t, Integer(1))}
    actual = generate_gate_rules(x*ph*cgate_t, return_as_muls=True)
    assert actual == gate_rules

    gate_rules = {((), (cgate_t**(-1), ph**(-1), x)),
                      ((), (ph**(-1), x, cgate_t**(-1))),
                      ((), (x, cgate_t**(-1), ph**(-1))),
                      ((cgate_t,), (ph**(-1), x)),
                      ((ph,), (x, cgate_t**(-1))),
                      ((x,), (cgate_t**(-1), ph**(-1))),
                      ((cgate_t, x), (ph**(-1),)),
                      ((ph, cgate_t), (x,)),
                      ((x, ph), (cgate_t**(-1),)),
                      ((cgate_t, x, ph), ()),
                      ((ph, cgate_t, x), ()),
                      ((x, ph, cgate_t), ())}
    actual = generate_gate_rules(x*ph*cgate_t)
    assert actual == gate_rules

