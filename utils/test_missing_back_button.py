
def test_missing_back_button():
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

    class Toolbar(NavigationToolbar2Tk):
        # Only display the buttons we need.
        toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                     t[0] in ('Home', 'Pan', 'Zoom')]

    fig = plt.figure()
    print("success")
    Toolbar(fig.canvas, fig.canvas.manager.window)  # This should not raise.
    print("success")

