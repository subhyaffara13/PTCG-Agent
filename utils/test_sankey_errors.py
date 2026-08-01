
def test_sankey_errors(kwargs, msg):
    with pytest.raises(ValueError, match=msg):
        Sankey(**kwargs)

