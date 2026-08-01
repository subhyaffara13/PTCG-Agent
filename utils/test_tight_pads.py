
def test_tight_pads():
    fig, ax = plt.subplots()
    with pytest.warns(PendingDeprecationWarning,
                      match='will be deprecated'):
        fig.set_tight_layout({'pad': 0.15})
    fig.draw_without_rendering()

