
def test_generate_equivalent_ids_2():
    # Test with Muls
    (x, y, z, h) = create_gate_sequence()

    assert generate_equivalent_ids((x,), return_as_muls=True) == {x}

    gate_ids = {Integer(1)}
    assert generate_equivalent_ids(x*x, return_as_muls=True) == gate_ids

    gate_ids = {x*y, y*x}
    assert generate_equivalent_ids(x*y, return_as_muls=True) == gate_ids

    gate_ids = {(x, y), (y, x)}
    assert generate_equivalent_ids(x*y) == gate_ids

    circuit = Mul(*(x, y, z))
    gate_ids = {x*y*z, y*z*x, z*x*y, z*y*x,
                    y*x*z, x*z*y}
    assert generate_equivalent_ids(circuit, return_as_muls=True) == gate_ids

    circuit = Mul(*(x, y, z, h))
    gate_ids = {x*y*z*h, y*z*h*x,
                    h*x*y*z, h*z*y*x,
                    z*y*x*h, y*x*h*z,
                    z*h*x*y, x*h*z*y}
    assert generate_equivalent_ids(circuit, return_as_muls=True) == gate_ids

    circuit = Mul(*(x, y, x, y))
    gate_ids = {x*y*x*y, y*x*y*x}
    assert generate_equivalent_ids(circuit, return_as_muls=True) == gate_ids

    cgate_y = CGate((1,), y)
    circuit = Mul(*(y, cgate_y, y, cgate_y))
    gate_ids = {y*cgate_y*y*cgate_y, cgate_y*y*cgate_y*y}
    assert generate_equivalent_ids(circuit, return_as_muls=True) == gate_ids

    cnot = CNOT(1, 0)
    cgate_z = CGate((0,), Z(1))
    circuit = Mul(*(cnot, h, cgate_z, h))
    gate_ids = {cnot*h*cgate_z*h, h*cgate_z*h*cnot,
                    h*cnot*h*cgate_z, cgate_z*h*cnot*h}
    assert generate_equivalent_ids(circuit, return_as_muls=True) == gate_ids

