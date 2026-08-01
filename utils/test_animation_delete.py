
def test_animation_delete(anim):
    if platform.python_implementation() == 'PyPy':
        # Something in the test setup fixture lingers around into the test and
        # breaks pytest.warns on PyPy. This garbage collection fixes it.
        # https://foss.heptapod.net/pypy/pypy/-/issues/3536
        np.testing.break_cycles()
    anim = animation.FuncAnimation(**anim)
    with pytest.warns(Warning, match='Animation was deleted'):
        del anim
        np.testing.break_cycles()

