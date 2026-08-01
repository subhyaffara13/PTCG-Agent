
def test_tight_kwargs():
    fig, ax = plt.subplots(tight_layout={'pad': 0.15})
    fig.draw_without_rendering()

