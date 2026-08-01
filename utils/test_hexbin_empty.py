
def test_hexbin_empty():
    # From #3886: creating hexbin from empty dataset raises ValueError
    fig, ax = plt.subplots()
    ax.hexbin([], [])
    # From #23922: creating hexbin with log scaling from empty
    # dataset raises ValueError
    ax.hexbin([], [], bins='log')
    # From #27103: np.max errors when handed empty data
    ax.hexbin([], [], C=[], reduce_C_function=np.max)
    # No string-comparison warning from NumPy.
    ax.hexbin([], [], bins=np.arange(10))

