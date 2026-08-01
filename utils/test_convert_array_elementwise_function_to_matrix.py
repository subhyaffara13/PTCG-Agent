
def test_convert_array_elementwise_function_to_matrix():

    d = Dummy("d")

    expr = ArrayElementwiseApplyFunc(Lambda(d, sin(d)), x.T*y)
    assert convert_array_to_matrix(expr) == sin(x.T*y)

    expr = ArrayElementwiseApplyFunc(Lambda(d, d**2), x.T*y)
    assert convert_array_to_matrix(expr) == (x.T*y)**2

    expr = ArrayElementwiseApplyFunc(Lambda(d, sin(d)), x)
    assert convert_array_to_matrix(expr).dummy_eq(x.applyfunc(sin))

    expr = ArrayElementwiseApplyFunc(Lambda(d, 1 / (2 * sqrt(d))), x)
    assert convert_array_to_matrix(expr) == S.Half * HadamardPower(x, -S.Half)

