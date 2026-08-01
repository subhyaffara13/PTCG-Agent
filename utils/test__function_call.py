
def test_FunctionCall():
    fc = FunctionCall('power', (x, 3))
    assert fc.function_args[0] == x
    assert fc.function_args[1] == 3
    assert len(fc.function_args) == 2
    assert isinstance(fc.function_args[1], Integer)
    assert fc == FunctionCall('power', (x, 3))
    assert fc != FunctionCall('power', (3, x))
    assert fc != FunctionCall('Power', (x, 3))
    assert fc.func(*fc.args) == fc

    fc2 = FunctionCall('fma', [2, 3, 4])
    assert len(fc2.function_args) == 3
    assert fc2.function_args[0] == 2
    assert fc2.function_args[1] == 3
    assert fc2.function_args[2] == 4
    assert str(fc2) in ( # not sure if QuotedString is a better default...
        'FunctionCall(fma, function_args=(2, 3, 4))',
        'FunctionCall("fma", function_args=(2, 3, 4))',
    )

