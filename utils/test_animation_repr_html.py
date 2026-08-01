
def test_animation_repr_html(writer, html, want, anim):
    if platform.python_implementation() == 'PyPy':
        # Something in the test setup fixture lingers around into the test and
        # breaks pytest.warns on PyPy. This garbage collection fixes it.
        # https://foss.heptapod.net/pypy/pypy/-/issues/3536
        np.testing.break_cycles()
    if (writer == 'imagemagick' and html == 'html5'
            # ImageMagick delegates to ffmpeg for this format.
            and not animation.FFMpegWriter.isAvailable()):
        pytest.skip('Requires FFMpeg')
    # create here rather than in the fixture otherwise we get __del__ warnings
    # about producing no output
    anim = animation.FuncAnimation(**anim)
    with plt.rc_context({'animation.writer': writer,
                         'animation.html': html}):
        html = anim._repr_html_()
    if want is None:
        assert html is None
        with pytest.warns(UserWarning):
            del anim  # Animation was never run, so will warn on cleanup.
            np.testing.break_cycles()
    else:
        assert want in html

