
def test_compressed1():
    fig, axs = plt.subplots(3, 2, layout='compressed',
                            sharex=True, sharey=True)
    for ax in axs.flat:
        pc = ax.imshow(np.random.randn(20, 20))

    fig.colorbar(pc, ax=axs)
    fig.draw_without_rendering()

    pos = axs[0, 0].get_position()
    np.testing.assert_allclose(pos.x0, 0.2381, atol=1e-2)
    pos = axs[0, 1].get_position()
    np.testing.assert_allclose(pos.x1, 0.7024, atol=1e-3)

    # wider than tall
    fig, axs = plt.subplots(2, 3, layout='compressed',
                            sharex=True, sharey=True, figsize=(5, 4))
    for ax in axs.flat:
        pc = ax.imshow(np.random.randn(20, 20))

    fig.colorbar(pc, ax=axs)
    fig.draw_without_rendering()

    pos = axs[0, 0].get_position()
    np.testing.assert_allclose(pos.x0, 0.05653, atol=1e-3)
    np.testing.assert_allclose(pos.y1, 0.8603, atol=1e-2)
    pos = axs[1, 2].get_position()
    np.testing.assert_allclose(pos.x1, 0.8728, atol=1e-3)
    np.testing.assert_allclose(pos.y0, 0.1808, atol=1e-2)

