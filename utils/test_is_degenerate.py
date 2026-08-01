
def test_is_degenerate():
    (x, y, z, h) = create_gate_sequence()

    gate_id = GateIdentity(x, y, z)
    ids = {gate_id}

    another_id = (z, y, x)
    assert is_degenerate(ids, another_id) is True

