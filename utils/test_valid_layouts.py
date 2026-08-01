
def test_valid_layouts():
    fig = Figure(layout=None)
    assert not fig.get_tight_layout()
    assert not fig.get_constrained_layout()

    fig = Figure(layout='tight')
    assert fig.get_tight_layout()
    assert not fig.get_constrained_layout()

    fig = Figure(layout='constrained')
    assert not fig.get_tight_layout()
    assert fig.get_constrained_layout()

