
def test_small_directed_sequences():
    dout = [5, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    din = [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1]
    assert nx.is_digraphical(din, dout)
    # Test nongraphical directed sequence
    dout = [1000, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    din = [103, 102, 102, 102, 102, 102, 102, 102, 102, 102]
    assert not nx.is_digraphical(din, dout)
    # Test digraphical small sequence
    dout = [1, 1, 1, 1, 1, 2, 2, 2, 3, 4]
    din = [2, 2, 2, 2, 2, 2, 2, 2, 1, 1]
    assert nx.is_digraphical(din, dout)
    # Test nonmatching sum
    din = [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]
    assert not nx.is_digraphical(din, dout)
    # Test for negative integer in sequence
    din = [2, 2, 2, -2, 2, 2, 2, 2, 1, 1, 4]
    assert not nx.is_digraphical(din, dout)
    # Test for noninteger
    din = dout = [1, 1, 1.1, 1]
    assert not nx.is_digraphical(din, dout)
    din = dout = [1, 1, "rer", 1]
    assert not nx.is_digraphical(din, dout)

