
def test_raises_networkxexception():
    with pytest.raises(nx.NetworkXException):
        raise nx.NetworkXException

