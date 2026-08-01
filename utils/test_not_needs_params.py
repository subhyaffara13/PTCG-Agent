
def test_not_needs_params(xp, window, winstr):
    if is_jax(xp) and winstr in ['taylor']:
        pytest.skip(reason=f'{winstr}: item assignment')
    win = get_window(winstr, 7, xp=xp)
    assert win.shape[0] == 7

