
def test_suptitle():
    fig, _ = plt.subplots()
    fig.suptitle('hello', color='r')
    fig.suptitle('title', color='g', rotation=30)


def test_suptitle():
    fig, ax = plt.subplots(tight_layout=True)
    st = fig.suptitle("foo")
    t = ax.set_title("bar")
    fig.canvas.draw()
    assert st.get_window_extent().y0 > t.get_window_extent().y1

