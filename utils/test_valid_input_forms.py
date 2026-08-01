
def test_valid_input_forms():
    fig, ax = plt.subplots()
    # These should not raise an error.
    ax.set_prop_cycle(None)
    ax.set_prop_cycle(cycler('linewidth', [1, 2]))
    ax.set_prop_cycle('color', 'rgywkbcm')
    ax.set_prop_cycle('lw', (1, 2))
    ax.set_prop_cycle('linewidth', [1, 2])
    ax.set_prop_cycle('linewidth', iter([1, 2]))
    ax.set_prop_cycle('linewidth', np.array([1, 2]))
    ax.set_prop_cycle('color', np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1]]))
    ax.set_prop_cycle('dashes', [[], [13, 2], [8, 3, 1, 3]])
    ax.set_prop_cycle(lw=[1, 2], color=['k', 'w'], ls=['-', '--'])
    ax.set_prop_cycle(lw=np.array([1, 2]),
                      color=np.array(['k', 'w']),
                      ls=np.array(['-', '--']))

