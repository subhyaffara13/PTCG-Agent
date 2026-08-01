
def test_resample_nonaffine(data, interpolation, expected, nonaffine_identity):
    # Test that both affine and nonaffine transforms resample to the correct answer

    # If the array is constant, the tolerance can be tight
    # Otherwise, the tolerance is limited by the subpixel approach in the agg backend
    atol = 0 if np.all(data == data.ravel()[0]) else 2e-3

    # Create a simple affine transform for scaling the input array
    affine_transform = Affine2D().scale(sx=expected.shape[1] / data.shape[1], sy=1)

    affine_result = np.empty_like(expected)
    mimage.resample(data, affine_result, affine_transform, interpolation=interpolation)
    assert_allclose(affine_result, expected, atol=atol)

    # Create a nonaffine version of the same transform
    # by compositing with a nonaffine identity transform
    nonaffine_transform = nonaffine_identity + affine_transform

    nonaffine_result = np.empty_like(expected)
    mimage.resample(data, nonaffine_result, nonaffine_transform,
                    interpolation=interpolation)
    assert_allclose(nonaffine_result, expected, atol=atol)

