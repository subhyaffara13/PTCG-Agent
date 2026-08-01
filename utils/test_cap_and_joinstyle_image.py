
def test_cap_and_joinstyle_image():
    fig, ax = plt.subplots()
    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([-0.5, 2.5])

    x = np.array([0.0, 1.0, 0.5])
    ys = np.array([[0.0], [0.5], [1.0]]) + np.array([[0.0, 0.0, 1.0]])

    segs = np.zeros((3, 3, 2))
    segs[:, :, 0] = x
    segs[:, :, 1] = ys
    line_segments = LineCollection(segs, linewidth=[10, 15, 20])
    line_segments.set_capstyle("round")
    line_segments.set_joinstyle("miter")

    ax.add_collection(line_segments)
    ax.set_title('Line collection with customized caps and joinstyle')

