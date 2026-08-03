import re

def test_save_count_override_warnings_has_length(anim):

    save_count = 5
    frames = list(range(2))
    match_target = (
        f'You passed in an explicit {save_count=} '
        "which is being ignored in favor of "
        f"{len(frames)=}."
    )

    with pytest.warns(UserWarning, match=re.escape(match_target)):
        anim = animation.FuncAnimation(
            **{**anim, 'frames': frames, 'save_count': save_count}
        )
    assert anim._save_count == len(frames)
    anim._init_draw()

