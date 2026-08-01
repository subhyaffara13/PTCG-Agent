
def test_non_affine_caching():
    class AssertingNonAffineTransform(mtransforms.Transform):
        """
        This transform raises an assertion error when called when it
        shouldn't be and ``self.raise_on_transform`` is True.

        """
        input_dims = output_dims = 2
        is_affine = False

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.raise_on_transform = False
            self.underlying_transform = mtransforms.Affine2D().scale(10, 10)

        def transform_path_non_affine(self, path):
            assert not self.raise_on_transform, \
                'Invalidated affine part of transform unnecessarily.'
            return self.underlying_transform.transform_path(path)
        transform_path = transform_path_non_affine

        def transform_non_affine(self, path):
            assert not self.raise_on_transform, \
                'Invalidated affine part of transform unnecessarily.'
            return self.underlying_transform.transform(path)
        transform = transform_non_affine

    my_trans = AssertingNonAffineTransform()
    ax = plt.axes()
    plt.plot(np.arange(10), transform=my_trans + ax.transData)
    plt.draw()
    # enable the transform to raise an exception if it's non-affine transform
    # method is triggered again.
    my_trans.raise_on_transform = True
    ax.transAxes.invalidate()
    plt.draw()

