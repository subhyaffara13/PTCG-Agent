
def test_gejsv_invalid_job_arguments(kwargs):
    """Test invalid job arguments raise an Exception"""
    A = np.ones((2, 2), dtype=float)
    gejsv = get_lapack_funcs('gejsv', dtype=float)
    assert_raises(Exception, gejsv, A, **kwargs)

