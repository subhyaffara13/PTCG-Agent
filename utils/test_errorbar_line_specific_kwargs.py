
def test_errorbar_line_specific_kwargs():
    # Check that passing line-specific keyword arguments will not result in
    # errors.
    x = np.arange(5)
    y = np.arange(5)

    plotline, _, _ = plt.errorbar(x, y, xerr=1, yerr=1, ls='None',
                                  marker='s', fillstyle='full',
                                  drawstyle='steps-mid',
                                  dash_capstyle='round',
                                  dash_joinstyle='miter',
                                  solid_capstyle='butt',
                                  solid_joinstyle='bevel')
    assert plotline.get_fillstyle() == 'full'
    assert plotline.get_drawstyle() == 'steps-mid'

