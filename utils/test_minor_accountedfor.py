
def test_minor_accountedfor():
    with rc_context({'_internal.classic_mode': False}):
        fig, ax = plt.subplots(dpi=200, figsize=(6, 6))
        fig.canvas.draw()
        ax.tick_params(which='both', direction='out')

        bbaxis, bbspines, bbax, bbtb = color_boxes(fig, ax)
        bbaxis, bbspines, bbax, bbtb = color_boxes(fig, ax)
        targets = [[150.0, 108.88888888888886, 930.0, 11.111111111111114],
                   [138.8889, 119.9999, 11.1111, 960.0]]
        for n in range(2):
            targetbb = mtransforms.Bbox.from_bounds(*targets[n])
            assert_allclose(
                bbspines[n * 2].bounds, targetbb.bounds, atol=1e-2)

        fig, ax = plt.subplots(dpi=200, figsize=(6, 6))
        fig.canvas.draw()
        ax.tick_params(which='both', direction='out')
        ax.minorticks_on()
        ax.tick_params(axis='both', which='minor', length=30)
        fig.canvas.draw()
        bbaxis, bbspines, bbax, bbtb = color_boxes(fig, ax)
        targets = [[150.0, 36.66666666666663, 930.0, 83.33333333333334],
                   [66.6667, 120.0, 83.3333, 960.0]]

        for n in range(2):
            targetbb = mtransforms.Bbox.from_bounds(*targets[n])
            assert_allclose(
                bbspines[n * 2].bounds, targetbb.bounds, atol=1e-2)

