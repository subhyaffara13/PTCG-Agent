
def test_dpi_change_triggers_resize():
    """
    Test that _update_device_pixel_ratio recalculates figure.size_inches
    using the actual widget dimensions, so the render size matches the
    visible canvas area even when constrained by a layout manager.
    See issue #31126.
    """
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    root = tk.Tk()
    root.geometry("400x300")
    root.update_idletasks()

    fig = Figure(dpi=100)
    fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
    root.update_idletasks()

    actual_w = canvas.get_tk_widget().winfo_width()
    actual_h = canvas.get_tk_widget().winfo_height()
    assert actual_w > 0 and actual_h > 0

    # Simulate a 2x DPI change through _update_device_pixel_ratio.
    # Mock the platform-specific DPI query to return ratio=2.0.
    with patch.object(sys, 'platform', 'linux'), \
         patch.object(canvas._tkcanvas, 'winfo_fpixels',
                      return_value=192.0):
        canvas._update_device_pixel_ratio()

    # Verify the render size matches the actual widget size, NOT the
    # inflated physical size from get_width_height(physical=True).
    size = fig.get_size_inches()
    render_w = round(size[0] * fig.dpi)
    render_h = round(size[1] * fig.dpi)
    assert abs(render_w - actual_w) <= 2, \
        f"render width {render_w} != actual width {actual_w}"
    assert abs(render_h - actual_h) <= 2, \
        f"render height {render_h} != actual height {actual_h}"

    print("success")
    root.destroy()

