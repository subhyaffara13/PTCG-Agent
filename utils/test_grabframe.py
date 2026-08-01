
def test_grabframe(tmp_path, writer, frame_format, output):
    WriterClass = animation.writers[writer]

    if frame_format is not None:
        plt.rcParams["animation.frame_format"] = frame_format

    fig, ax = plt.subplots()

    dpi = None
    codec = None
    if writer == 'ffmpeg':
        # Issue #8253
        fig.set_size_inches((10.85, 9.21))
        dpi = 100.
        codec = 'h264'

    test_writer = WriterClass()
    with test_writer.saving(fig, tmp_path / output, dpi):
        # smoke test it works
        test_writer.grab_frame()
        for k in {'dpi', 'bbox_inches', 'format'}:
            with pytest.raises(
                    TypeError,
                    match=f"grab_frame got an unexpected keyword argument {k!r}"):
                test_writer.grab_frame(**{k: object()})

