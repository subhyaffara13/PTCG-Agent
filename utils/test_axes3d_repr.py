
def test_axes3d_repr():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_label('label')
    ax.set_title('title')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    assert repr(ax) == (
        "<Axes3D: label='label', "
        "title={'center': 'title'}, xlabel='x', ylabel='y', zlabel='z'>")

