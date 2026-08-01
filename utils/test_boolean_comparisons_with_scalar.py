
def test_boolean_comparisons_with_scalar():
    rng = np.random.default_rng(23409823)
    a = random_array((5,4,8,7), density=0.6, random_state=rng, dtype=int)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SparseEfficiencyWarning)
        assert_equal((a==0).toarray(), a.toarray()==0)
        assert_equal((a!=0).toarray(), a.toarray()!=0)
        assert_equal((a>=1).toarray(), a.toarray()>=1)
        assert_equal((a<=1).toarray(), a.toarray()<=1)
        assert_equal((a>0).toarray(), a.toarray()>0)
        assert_equal((a<0).toarray(), a.toarray()<0)

