
def test_transform_with_zero_derivatives():
    # The transform is really a 45° rotation
    #     tr(x, y) = x-y, x+y; inv_tr(u, v) = (u+v)/2, (u-v)/2
    # with an additional x->exp(-x**-2) on each coordinate.
    # Therefore all ticks should be at +/-45°, even the one at zero where the
    # transform derivatives are zero.

    # at x=0, exp(-x**-2)=0; div-by-zero can be ignored.
    @np.errstate(divide="ignore")
    def tr(x, y):
        return np.exp(-x**-2) - np.exp(-y**-2), np.exp(-x**-2) + np.exp(-y**-2)

    def inv_tr(u, v):
        return (-np.log((u+v)/2))**(1/2), (-np.log((v-u)/2))**(1/2)

    fig = plt.figure()
    ax = fig.add_subplot(
        axes_class=FloatingAxes, grid_helper=GridHelperCurveLinear(
            (tr, inv_tr), extremes=(0, 10, 0, 10)))
    fig.canvas.draw()

    for k in ax.axis:
        for l, a in ax.axis[k].major_ticks.locs_angles:
            assert a % 90 == pytest.approx(45, abs=1e-3)

