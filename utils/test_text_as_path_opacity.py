
def test_text_as_path_opacity():
    plt.figure()
    plt.gca().set_axis_off()
    plt.text(0.25, 0.25, 'c', color=(0, 0, 0, 0.5))
    plt.text(0.25, 0.5, 'a', alpha=0.5)
    plt.text(0.25, 0.75, 'x', alpha=0.5, color=(0, 0, 0, 1))

