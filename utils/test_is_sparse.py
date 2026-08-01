
def test_is_sparse(check_scipy):
    msg = "is_sparse is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        assert com.is_sparse(SparseArray([1, 2, 3]))

        assert not com.is_sparse(np.array([1, 2, 3]))

        if check_scipy:
            import scipy.sparse

            assert not com.is_sparse(scipy.sparse.bsr_matrix([1, 2, 3]))

