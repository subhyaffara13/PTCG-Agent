
def test_mollweide_forward_inverse_closure():
    # test that the round-trip Mollweide forward->inverse transformation is an
    # approximate identity
    fig = plt.figure()
    ax = fig.add_subplot(projection='mollweide')

    # set up 1-degree grid in longitude, latitude
    lon = np.linspace(-np.pi, np.pi, 360)
    # The poles are degenerate and thus sensitive to floating point precision errors
    lat = np.linspace(-np.pi / 2.0, np.pi / 2.0, 180)[1:-1]
    lon, lat = np.meshgrid(lon, lat)
    ll = np.vstack((lon.flatten(), lat.flatten())).T

    # perform forward transform
    xy = ax.transProjection.transform(ll)

    # perform inverse transform
    ll2 = ax.transProjection.inverted().transform(xy)

    # compare
    np.testing.assert_array_almost_equal(ll, ll2, 3)

