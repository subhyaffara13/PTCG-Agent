
def test_colors_mixed(align, exp):
    data = DataFrame([[-1], [3]])
    result = data.style.bar(align=align, color=["red", "green"])._compute().ctx
    assert result == {(0, 0): exp[0], (1, 0): exp[1]}

