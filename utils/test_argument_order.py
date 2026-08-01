
def test_argument_order():
    expr = x + y
    routine = make_routine("test", expr, argument_sequence=[z, x, y], language="rust")
    code_gen = RustCodeGen()
    output = StringIO()
    code_gen.dump_rs([routine], output, "test", header=False, empty=False)
    source = output.getvalue()
    expected = (
        "fn test(z: f64, x: f64, y: f64) -> f64 {\n"
        "    let out1 = x + y;\n"
        "    out1\n"
        "}\n"
    )
    assert source == expected


def test_argument_order():
    mpl.rcParams['mathtext.fontset'] = 'cm'
    test_str = r'abc$abc\alpha$'
    fig, ax = plt.subplots()

    text1 = fig.text(0.1, 0.1, test_str,
                     math_fontfamily='dejavusans', font='Arial')
    prop1 = text1.get_fontproperties()
    assert prop1.get_math_fontfamily() == 'dejavusans'
    text2 = fig.text(0.2, 0.2, test_str,
                     math_fontfamily='dejavusans', fontproperties='Arial')
    prop2 = text2.get_fontproperties()
    assert prop2.get_math_fontfamily() == 'dejavusans'
    text3 = fig.text(0.3, 0.3, test_str,
                     font='Arial', math_fontfamily='dejavusans')
    prop3 = text3.get_fontproperties()
    assert prop3.get_math_fontfamily() == 'dejavusans'
    text4 = fig.text(0.4, 0.4, test_str,
                     fontproperties='Arial', math_fontfamily='dejavusans')
    prop4 = text4.get_fontproperties()
    assert prop4.get_math_fontfamily() == 'dejavusans'

    fig.draw_without_rendering()

