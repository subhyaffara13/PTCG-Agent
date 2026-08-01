
def test_yen_source_sink_validation(source, sink):
    # directed_G has shape (6, 6)
    with pytest.raises(ValueError, match="must have 0 <="):
        yen(directed_G, source, sink, 2)

