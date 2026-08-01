
def test_LineOver1DRangeSeries_complex_range():
    # verify that LineOver1DRangeSeries can accept a complex range
    # if the imaginary part of the start and end values are the same

    x = symbols("x")

    LineOver1DRangeSeries(sqrt(x), (x, -10, 10))
    LineOver1DRangeSeries(sqrt(x), (x, -10-2j, 10-2j))
    raises(ValueError,
        lambda : LineOver1DRangeSeries(sqrt(x), (x, -10-2j, 10+2j)))

