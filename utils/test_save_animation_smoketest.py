
def test_save_animation_smoketest(tmp_path, writer, frame_format, output, anim):
    if frame_format is not None:
        plt.rcParams["animation.frame_format"] = frame_format
    anim = animation.FuncAnimation(**anim)
    dpi = None
    codec = None
    if writer == 'ffmpeg':
        # Issue #8253
        anim._fig.set_size_inches((10.85, 9.21))
        dpi = 100.
        codec = 'h264'

    anim.save(tmp_path / output, fps=30, writer=writer, bitrate=500, dpi=dpi,
              codec=codec)

    del anim

