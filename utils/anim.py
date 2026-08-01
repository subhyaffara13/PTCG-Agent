
def anim(request):
    """Create a simple animation (with options)."""
    fig, ax = plt.subplots()
    line, = ax.plot([], [])

    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x = np.linspace(0, 10, 100)
        y = np.sin(x + i)
        line.set_data(x, y)
        return line,

    # "klass" can be passed to determine the class returned by the fixture
    kwargs = dict(getattr(request, 'param', {}))  # make a copy
    klass = kwargs.pop('klass', animation.FuncAnimation)
    if 'frames' not in kwargs:
        kwargs['frames'] = 5
    return klass(fig=fig, func=animate, init_func=init, **kwargs)

