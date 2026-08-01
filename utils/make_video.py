
def make_video(tensor, fps):
    try:
        import moviepy  # noqa: F401
    except ImportError:
        print("add_video needs package moviepy")
        return
    try:
        from moviepy import editor as mpy
    except ImportError:
        print(
            "moviepy is installed, but can't import moviepy.editor.",
            "Some packages could be missing [imageio, requests]",
        )
        return
    import tempfile

    _t, h, w, c = tensor.shape

    # encode sequence of images into gif string
    clip = mpy.ImageSequenceClip(list(tensor), fps=fps)

    with tempfile.NamedTemporaryFile(suffix=".gif") as f:
        filename = f.name
        try:  # newer version of moviepy use logger instead of progress_bar argument.
            clip.write_gif(filename, verbose=False, logger=None)
        except TypeError:
            try:  # older version of moviepy does not support progress_bar argument.
                clip.write_gif(filename, verbose=False, progress_bar=False)
            except TypeError:
                clip.write_gif(filename, verbose=False)

        f.seek(0)
        tensor_string = f.read()

        return Summary.Image(
            height=h, width=w, colorspace=c, encoded_image_string=tensor_string
        )

