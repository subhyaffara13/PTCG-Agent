
def test_resample_dtypes(dtype, ndim):
    # Issue 28448, incorrect dtype comparisons in C++ image_resample can raise
    # ValueError: arrays must be of dtype byte, short, float32 or float64
    rng = np.random.default_rng(4181)
    shape = (2, 2) if ndim == 2 else (2, 2, 3)
    data = rng.uniform(size=shape).astype(np.dtype(dtype, copy=True))
    fig, ax = plt.subplots()
    axes_image = ax.imshow(data)
    # Before fix the following raises ValueError for some dtypes.
    axes_image.make_image(None)[0]

