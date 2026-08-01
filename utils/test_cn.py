
def test_cn():
    matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                    ['blue', 'r'])
    assert mcolors.to_hex("C0") == '#0000ff'
    assert mcolors.to_hex("C1") == '#ff0000'

    matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                    ['xkcd:blue', 'r'])
    assert mcolors.to_hex("C0") == '#0343df'
    assert mcolors.to_hex("C1") == '#ff0000'
    assert mcolors.to_hex("C10") == '#0343df'
    assert mcolors.to_hex("C11") == '#ff0000'

    matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['8e4585', 'r'])

    assert mcolors.to_hex("C0") == '#8e4585'
    # if '8e4585' gets parsed as a float before it gets detected as a hex
    # colour it will be interpreted as a very large number.
    # this mustn't happen.
    assert mcolors.to_rgb("C0")[0] != np.inf

