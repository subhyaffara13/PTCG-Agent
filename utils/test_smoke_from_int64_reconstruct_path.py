
def test_smoke_from_int64_reconstruct_path(A):
    pred = np.array([-9999, 0, 1])
    reconstruct_path(A, pred)

