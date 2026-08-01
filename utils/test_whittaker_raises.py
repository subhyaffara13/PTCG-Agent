
def test_whittaker_raises(signal, lamb, order, weights, err, msg):
    """Test that whittaker raises errors."""
    with pytest.raises(err, match=msg):
        whittaker_henderson(signal, lamb=lamb, order=order, weights=weights)

