
def test_constrained_toggle():
    fig, ax = plt.subplots()
    with pytest.warns(PendingDeprecationWarning):
        fig.set_constrained_layout(True)
        assert fig.get_constrained_layout()
        fig.set_constrained_layout(False)
        assert not fig.get_constrained_layout()
        fig.set_constrained_layout(True)
        assert fig.get_constrained_layout()

