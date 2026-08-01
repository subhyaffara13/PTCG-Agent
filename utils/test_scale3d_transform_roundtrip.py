
def test_scale3d_transform_roundtrip(scale_type):
    """Forward/inverse transform should preserve values."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xscale=scale_type, yscale=scale_type, zscale=scale_type)

    # Use appropriate test values for each scale type
    test_values = {
        'log': [1, 10, 100, 1000],
        'symlog': [-100, -1, 0, 1, 100],
        'asinh': [-100, -1, 0, 1, 100],
        'logit': [0.01, 0.1, 0.5, 0.9, 0.99],
    }[scale_type]
    test_values = np.array(test_values)

    # Test round-trip for each axis
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        trans = axis.get_transform()
        forward = trans.transform(test_values.reshape(-1, 1))
        inverse = trans.inverted().transform(forward)
        np.testing.assert_allclose(inverse.flatten(), test_values, rtol=1e-10)

