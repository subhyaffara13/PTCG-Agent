
def test_has_alpha_channel():
    assert mcolors._has_alpha_channel((0, 0, 0, 0))
    assert mcolors._has_alpha_channel([1, 1, 1, 1])
    assert mcolors._has_alpha_channel('#fff8')
    assert mcolors._has_alpha_channel('#0f0f0f80')
    assert mcolors._has_alpha_channel(('r', 0.5))
    assert mcolors._has_alpha_channel(([1, 1, 1, 1], None))
    assert not mcolors._has_alpha_channel('blue')  # 4-char string!
    assert not mcolors._has_alpha_channel('0.25')
    assert not mcolors._has_alpha_channel('r')
    assert not mcolors._has_alpha_channel((1, 0, 0))
    assert not mcolors._has_alpha_channel('#fff')
    assert not mcolors._has_alpha_channel('#0f0f0f')
    assert not mcolors._has_alpha_channel(('r', None))
    assert not mcolors._has_alpha_channel(([1, 1, 1], None))

