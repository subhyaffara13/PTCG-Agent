
def test_set_constrained_layout(arg, state):
    fig, ax = plt.subplots(constrained_layout=arg)
    assert fig.get_constrained_layout() is state

