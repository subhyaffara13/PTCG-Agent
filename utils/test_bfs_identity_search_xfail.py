
def test_bfs_identity_search_xfail():
    s = PhaseGate(0)
    t = TGate(0)
    gate_list = [Dagger(s), t]
    id_set = {GateIdentity(Dagger(s), t, t)}
    assert bfs_identity_search(gate_list, 1, max_depth=3) == id_set

