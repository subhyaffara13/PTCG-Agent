
def test_golden_ratio_rewrite_as_sqrt():
    assert GoldenRatio.rewrite(sqrt) == S.Half + sqrt(5)*S.Half

