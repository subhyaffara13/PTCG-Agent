
def test_remove_shared_axes(shared_axes_generator, shared_axis_remover):
    # test all of the ways to get fig/ax sets
    fig, ax = shared_axes_generator
    shared_axis_remover(ax)

