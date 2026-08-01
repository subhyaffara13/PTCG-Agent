
def test_fft_peaks():
    fig, ax = plt.subplots()
    t = np.arange(65536)
    p1 = ax.plot(abs(np.fft.fft(np.sin(2*np.pi*.01*t)*np.blackman(len(t)))))

    # Ensure that the path's transform takes the new axes limits into account.
    fig.canvas.draw()
    path = p1[0].get_path()
    transform = p1[0].get_transform()
    path = transform.transform_path(path)
    simplified = path.cleaned(simplify=True)

    assert simplified.vertices.size == 36

