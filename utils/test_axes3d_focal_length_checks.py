
def test_axes3d_focal_length_checks():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    with pytest.raises(ValueError):
        ax.set_proj_type('persp', focal_length=0)
    with pytest.raises(ValueError):
        ax.set_proj_type('ortho', focal_length=1)

