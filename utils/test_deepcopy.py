
def test_deepcopy(xp):
    r = Rotation.from_quat(xp.asarray([0, 0, math.sin(np.pi/4), math.cos(np.pi/4)]))
    r1 = copy.deepcopy(r)
    xp_assert_close(r.as_matrix(), r1.as_matrix(), atol=1e-15)


def test_deepcopy():
    with pytest.raises(TypeError, match="Expression objects are not copiable"):
        copy.deepcopy(pd.col("a"))


def test_deepcopy():
    fig1, ax = plt.subplots()
    ax.plot([0, 1], [2, 3])
    ax.set_yscale('log')

    fig2 = copy.deepcopy(fig1)

    # Make sure it is a new object
    assert fig2.axes[0] is not ax
    # And that the axis scale got propagated
    assert fig2.axes[0].get_yscale() == 'log'
    # Update the deepcopy and check the original isn't modified
    fig2.axes[0].set_yscale('linear')
    assert ax.get_yscale() == 'log'

    # And test the limits of the axes don't get propagated
    ax.set_xlim(1e-1, 1e2)
    # Draw these to make sure limits are updated
    fig1.draw_without_rendering()
    fig2.draw_without_rendering()

    assert ax.get_xlim() == (1e-1, 1e2)
    assert fig2.axes[0].get_xlim() == (0, 1)

