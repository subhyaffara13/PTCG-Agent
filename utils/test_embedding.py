
def test_embedding():
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure

    root = tk.Tk()

    def test_figure(master):
        fig = Figure()
        ax = fig.add_subplot()
        ax.plot([1, 2, 3])

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.mpl_connect("key_press_event", key_press_handler)
        canvas.get_tk_widget().pack(expand=True, fill="both")

        toolbar = NavigationToolbar2Tk(canvas, master, pack_toolbar=False)
        toolbar.pack(expand=True, fill="x")

        canvas.get_tk_widget().forget()
        toolbar.forget()

    test_figure(root)
    print("success")

    # Test with a dark button color. Doesn't actually check whether the icon
    # color becomes lighter, just that the code doesn't break.

    root.tk_setPalette(background="sky blue", selectColor="midnight blue",
                       foreground="white")
    test_figure(root)
    print("success")

