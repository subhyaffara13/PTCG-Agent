
def test_ndarray_subclass_norm():
    # Emulate an ndarray subclass that handles units
    # which objects when adding or subtracting with other
    # arrays. See #6622 and #8696
    class MyArray(np.ndarray):
        def __isub__(self, other):  # type: ignore[misc]
            raise RuntimeError

        def __add__(self, other):
            raise RuntimeError

    data = np.arange(-10, 10, 1, dtype=float).reshape((10, 2))
    mydata = data.view(MyArray)

    for norm in [mcolors.Normalize(), mcolors.LogNorm(),
                 mcolors.SymLogNorm(3, vmax=5, linscale=1, base=np.e),
                 mcolors.Normalize(vmin=mydata.min(), vmax=mydata.max()),
                 mcolors.SymLogNorm(3, vmin=mydata.min(), vmax=mydata.max(),
                                    base=np.e),
                 mcolors.PowerNorm(1)]:
        assert_array_equal(norm(mydata), norm(data))
        fig, ax = plt.subplots()
        ax.imshow(mydata, norm=norm)
        fig.canvas.draw()  # Check that no warning is emitted.

