
def test_set_drawstyle():
    x = np.linspace(0, 2*np.pi, 10)
    y = np.sin(x)

    fig, ax = plt.subplots()
    line, = ax.plot(x, y)
    line.set_drawstyle("steps-pre")
    assert len(line.get_path().vertices) == 2*len(x)-1

    line.set_drawstyle("default")
    assert len(line.get_path().vertices) == len(x)

