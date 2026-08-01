
def test_no_empty_apply(mi_styler):
    # 45313
    mi_styler.apply(lambda s: ["a:v;"] * 2, subset=[False, False])
    mi_styler._compute()

