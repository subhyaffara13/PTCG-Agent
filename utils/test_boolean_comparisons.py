
def test_boolean_comparisons(a_shape, b_shape):
    rng = np.random.default_rng(23409823)
    a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SparseEfficiencyWarning)
        assert_equal((a==b).toarray(), a.toarray()==b.toarray())
        assert_equal((a!=b).toarray(), a.toarray()!=b.toarray())
        assert_equal((a>=b).toarray(), a.toarray()>=b.toarray())
        assert_equal((a<=b).toarray(), a.toarray()<=b.toarray())
        assert_equal((a>b).toarray(), a.toarray()>b.toarray())
        assert_equal((a<b).toarray(), a.toarray()<b.toarray())
        assert_equal((a==b).toarray(), np.bitwise_not((a!=b).toarray()))
        assert_equal((a>=b).toarray(), np.bitwise_not((a<b).toarray()))
        assert_equal((a<=b).toarray(), np.bitwise_not((a>b).toarray()))

