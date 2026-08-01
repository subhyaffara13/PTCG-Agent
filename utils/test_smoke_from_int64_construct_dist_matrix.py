
def test_smoke_from_int64_construct_dist_matrix(A):
    _, preds = shortest_path(A, return_predecessors=True)
    construct_dist_matrix(A, preds)

