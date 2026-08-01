
def test_update_mutate_input():
    inp = dict(fontproperties=FontProperties(weight="bold"),
               bbox=None)
    cache = dict(inp)
    t = Text()
    t.update(inp)
    assert inp['fontproperties'] == cache['fontproperties']
    assert inp['bbox'] == cache['bbox']

