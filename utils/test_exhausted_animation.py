
def test_exhausted_animation(tmp_path):
    fig, ax = plt.subplots()

    def update(frame):
        return []

    anim = animation.FuncAnimation(
        fig, update, frames=iter(range(10)), repeat=False,
        cache_frame_data=False
    )

    anim.save(tmp_path / "test.gif", writer='pillow')

    with pytest.warns(UserWarning, match="exhausted"):
        anim._start()

