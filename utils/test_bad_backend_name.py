
def test_bad_backend_name():
    """Using `backend=` raises with unknown backend even if there are no backends."""
    with pytest.raises(
        ImportError, match="'this_backend_does_not_exist' backend is not installed"
    ):
        nx.null_graph(backend="this_backend_does_not_exist")

