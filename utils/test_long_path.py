
def test_long_path():
    buff = io.BytesIO()
    fig = Figure()
    ax = fig.subplots()
    points = np.ones(100_000)
    points[::2] *= -1
    ax.plot(points)
    fig.savefig(buff, format='png')

