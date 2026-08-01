
def test_format_error_message():
    with pytest.raises(ValueError, match="Invalid form: 'toto'"):
        _ = csgraph.laplacian(np.eye(1), form='toto')

