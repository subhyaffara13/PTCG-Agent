
def test_never_update():
    import tkinter
    del tkinter.Misc.update
    del tkinter.Misc.update_idletasks

    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.show(block=False)

    plt.draw()  # Test FigureCanvasTkAgg.
    tool = fig.canvas.toolbar.configure_subplots()  # Test NavigationToolbar2Tk.
    assert tool is not None
    assert tool == fig.canvas.toolbar.configure_subplots()  # Tool is reused internally.
    # Test FigureCanvasTk filter_destroy callback
    fig.canvas.get_tk_widget().after(100, plt.close, fig)

    # Check for update() or update_idletasks() in the event queue, functionally
    # equivalent to tkinter.Misc.update.
    plt.show(block=True)

