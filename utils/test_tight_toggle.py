
def test_tight_toggle():
    fig, ax = plt.subplots()
    with pytest.warns(PendingDeprecationWarning):
        fig.set_tight_layout(True)
        assert fig.get_tight_layout()
        fig.set_tight_layout(False)
        assert not fig.get_tight_layout()
        fig.set_tight_layout(True)
        assert fig.get_tight_layout()

