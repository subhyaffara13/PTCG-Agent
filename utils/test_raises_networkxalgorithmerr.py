
def test_raises_networkxalgorithmerr():
    with pytest.raises(nx.NetworkXAlgorithmError):
        raise nx.NetworkXAlgorithmError

