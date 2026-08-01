
def test_logit_scales():
    fig, ax = plt.subplots()

    # Typical extinction curve for logit
    x = np.array([0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5,
                  0.6, 0.7, 0.8, 0.9, 0.97, 0.99, 0.997, 0.999])
    y = 1.0 / x

    ax.plot(x, y)
    ax.set_xscale('logit')
    ax.grid(True)
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    assert np.isfinite(bbox.x0)
    assert np.isfinite(bbox.y0)

