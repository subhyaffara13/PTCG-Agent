
def test_arrow_set_data():
    fig, ax = plt.subplots()
    arrow = mpl.patches.Arrow(2, 0, 0, 10)
    expected1 = np.array(
       [[1.9,  0.],
        [2.1, -0.],
        [2.1, 8.],
        [2.3, 8.],
        [2., 10.],
        [1.7, 8.],
        [1.9, 8.],
        [1.9, 0.]]
    )
    assert np.allclose(expected1, np.round(arrow.get_verts(), 2))

    expected2 = np.array(
        [[0.39, 0.04],
         [0.61, -0.04],
         [3.01, 6.36],
         [3.24, 6.27],
         [3.5, 8.],
         [2.56, 6.53],
         [2.79, 6.44],
         [0.39, 0.04]]
    )
    arrow.set_data(x=.5, dx=3, dy=8, width=1.2)
    assert np.allclose(expected2, np.round(arrow.get_verts(), 2))

