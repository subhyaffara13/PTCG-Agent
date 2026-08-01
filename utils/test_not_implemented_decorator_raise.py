
def test_not_implemented_decorator_raise():
    with pytest.raises(nx.NetworkXNotImplemented):

        @not_implemented_for("graph")
        def test1(G):
            pass

        test1(nx.Graph())

