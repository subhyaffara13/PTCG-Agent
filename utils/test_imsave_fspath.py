
def test_imsave_fspath(fmt, tmp_path):
    plt.imsave(tmp_path / f'unused.{fmt}', np.array([[0, 1]]), format=fmt)

