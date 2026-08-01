
def test_not_implemented_decorator_key():
    with pytest.raises(KeyError):

        @not_implemented_for("foo")
        def test1(G):
            pass

        test1(nx.Graph())

