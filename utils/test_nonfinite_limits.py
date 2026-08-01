
def test_nonfinite_limits():
    x = np.arange(0., np.e, 0.01)
    # silence divide by zero warning from log(0)
    with np.errstate(divide='ignore'):
        y = np.log(x)
    x[len(x)//2] = np.nan
    fig, ax = plt.subplots()
    ax.plot(x, y)

