
def assert_is_valid_plot_return_object(objs) -> None:
    from matplotlib.artist import Artist
    from matplotlib.axes import Axes

    if isinstance(objs, (Series, np.ndarray)):
        if isinstance(objs, Series):
            objs = objs._values
        for el in objs.reshape(-1):
            msg = (
                "one of 'objs' is not a matplotlib Axes instance, "
                f"type encountered {type(el).__name__!r}"
            )
            assert isinstance(el, (Axes, dict)), msg
    else:
        msg = (
            "objs is neither an ndarray of Artist instances nor a single "
            "ArtistArtist instance, tuple, or dict, 'objs' is a "
            f"{type(objs).__name__!r}"
        )
        assert isinstance(objs, (Artist, tuple, dict)), msg

