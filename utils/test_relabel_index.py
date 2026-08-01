
def test_relabel_index(styler_multi):
    labels = [(1, 2), (3, 4)]
    styler_multi.hide(axis=0, subset=[("X", "x"), ("Y", "y")])
    styler_multi.relabel_index(labels=labels)
    ctx = styler_multi._translate(True, True)
    assert {"value": "X", "display_value": 1}.items() <= ctx["body"][0][0].items()
    assert {"value": "y", "display_value": 2}.items() <= ctx["body"][0][1].items()
    assert {"value": "Y", "display_value": 3}.items() <= ctx["body"][1][0].items()
    assert {"value": "x", "display_value": 4}.items() <= ctx["body"][1][1].items()

