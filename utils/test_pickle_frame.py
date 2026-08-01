
def test_pickle_frame():
    N = ReferenceFrame('N')
    A = ReferenceFrame('A')
    A.orient_axis(N, N.x, 1)
    A_C_N = A.dcm(N)
    N1 = pickle.loads(pickle.dumps(N))
    A1 = tuple(N1._dcm_dict.keys())[0]
    assert A1.dcm(N1) == A_C_N

