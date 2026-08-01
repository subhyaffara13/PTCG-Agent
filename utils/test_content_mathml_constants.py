
def test_content_mathml_constants():
    mml = mp._print(I)
    assert mml.nodeName == 'imaginaryi'

    mml = mp._print(E)
    assert mml.nodeName == 'exponentiale'

    mml = mp._print(oo)
    assert mml.nodeName == 'infinity'

    mml = mp._print(pi)
    assert mml.nodeName == 'pi'

    assert mathml(hbar) == '<hbar/>'
    assert mathml(S.TribonacciConstant) == '<tribonacciconstant/>'
    assert mathml(S.GoldenRatio) == '<cn>&#966;</cn>'
    mml = mathml(S.EulerGamma)
    assert mml == '<eulergamma/>'

    mml = mathml(S.EmptySet)
    assert mml == '<emptyset/>'

    mml = mathml(S.true)
    assert mml == '<true/>'

    mml = mathml(S.false)
    assert mml == '<false/>'

    mml = mathml(S.NaN)
    assert mml == '<notanumber/>'

