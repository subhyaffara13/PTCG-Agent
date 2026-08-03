import re

def test_disable_cache_warning(anim):
    cache_frame_data = True
    frames = iter(range(5))
    match_target = (
        f"{frames=!r} which we can infer the length of, "
        "did not pass an explicit *save_count* "
        f"and passed {cache_frame_data=}.  To avoid a possibly "
        "unbounded cache, frame data caching has been disabled. "
        "To suppress this warning either pass "
        "`cache_frame_data=False` or `save_count=MAX_FRAMES`."
    )
    with pytest.warns(UserWarning, match=re.escape(match_target)):
        anim = animation.FuncAnimation(
            **{**anim, 'cache_frame_data': cache_frame_data, 'frames': frames}
        )
    assert anim._cache_frame_data is False
    anim._init_draw()

