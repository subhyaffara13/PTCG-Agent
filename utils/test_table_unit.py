
def test_table_unit(fig_test, fig_ref):
    # test that table doesn't participate in unit machinery, instead uses repr/str

    class FakeUnit:
        def __init__(self, thing):
            pass
        def __repr__(self):
            return "Hello"

    fake_convertor = munits.ConversionInterface()
    # v, u, a = value, unit, axis
    fake_convertor.convert = Mock(side_effect=lambda v, u, a: 0)
    # not used, here for completeness
    fake_convertor.default_units = Mock(side_effect=lambda v, a: None)
    fake_convertor.axisinfo = Mock(side_effect=lambda u, a: munits.AxisInfo())

    munits.registry[FakeUnit] = fake_convertor

    data = [[FakeUnit("yellow"), FakeUnit(42)],
            [FakeUnit(datetime.datetime(1968, 8, 1)), FakeUnit(True)]]

    fig_test.subplots().table(data)
    fig_ref.subplots().table([["Hello", "Hello"], ["Hello", "Hello"]])
    fig_test.canvas.draw()
    fake_convertor.convert.assert_not_called()

    munits.registry.pop(FakeUnit)
    assert not munits.registry.get_converter(FakeUnit)

