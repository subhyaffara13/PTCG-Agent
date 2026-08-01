
def test_issue_17616():
    assert pretty(pi**(1/exp(1))) == \
   '  / -1\\\n'\
   '  \\e  /\n'\
   'pi     '

    assert upretty(pi**(1/exp(1))) == \
   ' ⎛ -1⎞\n'\
   ' ⎝ℯ  ⎠\n'\
   'π     '

    assert pretty(pi**(1/pi)) == \
    '  1 \n'\
    '  --\n'\
    '  pi\n'\
    'pi  '

    assert upretty(pi**(1/pi)) == \
    ' 1\n'\
    ' ─\n'\
    ' π\n'\
    'π '

    assert pretty(pi**(1/EulerGamma)) == \
    '      1     \n'\
    '  ----------\n'\
    '  EulerGamma\n'\
    'pi          '

    assert upretty(pi**(1/EulerGamma)) == \
    ' 1\n'\
    ' ─\n'\
    ' γ\n'\
    'π '

    z = Symbol("x_17")
    assert upretty(7**(1/z)) == \
    'x₁₇___\n'\
    ' ╲╱ 7 '

    assert pretty(7**(1/z)) == \
    'x_17___\n'\
    '  \\/ 7 '

