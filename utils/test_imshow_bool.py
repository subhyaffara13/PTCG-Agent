
def test_imshow_bool():
    fig, ax = plt.subplots()
    ax.imshow(np.array([[True, False], [False, True]], dtype=bool))

