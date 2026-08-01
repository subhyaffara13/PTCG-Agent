
def test_from_graph6_raises_header_newline():
    """graph6 headers must not be followed by a newline. See gh-7557."""
    with pytest.raises(nx.NetworkXError):
        G = nx.from_graph6_bytes(b">>graph6<<\nP~~~~~~~~~~~~~~~~~~~~~~{")

