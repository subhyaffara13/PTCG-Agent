
def test_sankey_add_errors(kwargs, msg):
    sankey = Sankey()
    with pytest.raises(ValueError, match=msg):
        sankey.add(flows=[0.2, -0.2])
        sankey.add(**kwargs)

