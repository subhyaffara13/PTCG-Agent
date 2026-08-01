
def test_orientnew_respects_input_indices():
    N = ReferenceFrame('N')
    q1 = dynamicsymbols('q1')
    A = N.orientnew('a', 'Axis', [q1, N.z])
    #modify default indices:
    minds = [x+'1' for x in N.indices]
    B = N.orientnew('b', 'Axis', [q1, N.z], indices=minds)

    assert N.indices == A.indices
    assert B.indices == minds

