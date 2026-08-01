
def test_pie_hatch_multi(fig_test, fig_ref):
    x = [0.3, 0.3, 0.1]
    hatch = ['/', '+', '.']
    fig_test.subplots().pie(x, hatch=hatch)
    wedges, _ = fig_ref.subplots().pie(x)
    [w.set_hatch(hp) for w, hp in zip(wedges, hatch)]

