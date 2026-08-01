
def test_device_pixel_ratio_change():
    """
    Make sure that if the pixel ratio changes, the figure dpi changes but the
    widget remains the same logical size.
    """

    prop = 'matplotlib.backends.backend_qt.FigureCanvasQT.devicePixelRatioF'
    with mock.patch(prop) as p:
        p.return_value = 3

        fig = plt.figure(figsize=(5, 2), dpi=120)
        qt_canvas = fig.canvas
        qt_canvas.show()

        def set_device_pixel_ratio(ratio):
            p.return_value = ratio

            window = qt_canvas.window().windowHandle()
            current_version = tuple(int(x) for x in QtCore.qVersion().split('.', 2)[:2])
            if current_version >= (6, 6):
                QtCore.QCoreApplication.sendEvent(
                    window,
                    QtCore.QEvent(QtCore.QEvent.Type.DevicePixelRatioChange))
            else:
                # The value here doesn't matter, as we can't mock the C++ QScreen
                # object, but can override the functional wrapper around it.
                # Emitting this event is simply to trigger the DPI change handler
                # in Matplotlib in the same manner that it would occur normally.
                window.screen().logicalDotsPerInchChanged.emit(96)

            qt_canvas.draw()
            qt_canvas.flush_events()

            # Make sure the mocking worked
            assert qt_canvas.device_pixel_ratio == ratio

        qt_canvas.manager.show()
        qt_canvas.draw()
        qt_canvas.flush_events()
        size = qt_canvas.size()

        options = [
            (None, 360, 1800, 720),  # Use ratio at startup time.
            (3, 360, 1800, 720),  # Change to same ratio.
            (2, 240, 1200, 480),  # Change to different ratio.
            (1.5, 180, 900, 360),  # Fractional ratio.
        ]
        for ratio, dpi, width, height in options:
            if ratio is not None:
                set_device_pixel_ratio(ratio)

            # The DPI and the renderer width/height change
            assert fig.dpi == dpi
            assert qt_canvas.renderer.width == width
            assert qt_canvas.renderer.height == height

            # The actual widget size and figure logical size don't change.
            assert size.width() == 600
            assert size.height() == 240
            assert qt_canvas.get_width_height() == (600, 240)
            assert (fig.get_size_inches() == (5, 2)).all()

        # check that closing the figure restores the original dpi
        plt.close(fig)
        assert fig.dpi == 120

