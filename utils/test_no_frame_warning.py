
def test_no_frame_warning():
    fig, ax = plt.subplots()

    def update(frame):
        return []

    anim = animation.FuncAnimation(
        fig, update, frames=[], repeat=False,
        cache_frame_data=False
    )

    with pytest.warns(UserWarning, match="exhausted"):
        anim._start()

