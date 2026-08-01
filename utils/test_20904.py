
def test_20904(min_only, directed, return_predecessors, index_dtype, indices):
    """Test two failures from gh-20904: int32 and indices-as-None."""
    adj_mat = scipy.sparse.eye_array(4, format="csr")
    adj_mat = scipy.sparse.csr_array(
        (
            adj_mat.data,
            adj_mat.indices.astype(index_dtype),
            adj_mat.indptr.astype(index_dtype),
        ),
    )
    dijkstra(
        adj_mat,
        directed,
        indices=indices,
        min_only=min_only,
        return_predecessors=return_predecessors,
    )

