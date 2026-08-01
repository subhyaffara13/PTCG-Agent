
def test_log_scale_image():
    Z = np.zeros((10, 10))
    Z[::2] = 1

    fig, ax = plt.subplots()
    ax.imshow(Z, extent=[1, 100, 1, 100], cmap='viridis', vmax=1, vmin=-1,
              aspect='auto')
    ax.set(yscale='log')

