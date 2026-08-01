
def test_render_label():
    assert render_label('q0') == r'$\left|q0\right\rangle$'
    assert render_label('q0', {'q0': '0'}) == r'$\left|q0\right\rangle=\left|0\right\rangle$'

