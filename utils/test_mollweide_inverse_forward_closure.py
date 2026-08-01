
def test_mollweide_inverse_forward_closure():
    # test that the round-trip Mollweide inverse->forward transformation is an
    # approximate identity
    fig = plt.figure()
    ax = fig.add_subplot(projection='mollweide')

    # set up grid in x, y
    x = np.linspace(0, 1, 500)
    x, y = np.meshgrid(x, x)
    xy = np.vstack((x.flatten(), y.flatten())).T

    # perform inverse transform
    ll = ax.transProjection.inverted().transform(xy)

    # perform forward transform
    xy2 = ax.transProjection.transform(ll)

    # compare
    np.testing.assert_array_almost_equal(xy, xy2, 3)

