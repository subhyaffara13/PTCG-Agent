
def test_print_constants():
    assert mpp.doprint(hbar) == '<mi>&#x210F;</mi>'
    assert mpp.doprint(S.TribonacciConstant) == '<mi>TribonacciConstant</mi>'
    assert mpp.doprint(S.GoldenRatio) == '<mi>&#x3A6;</mi>'
    assert mpp.doprint(S.EulerGamma) == '<mi>&#x3B3;</mi>'

