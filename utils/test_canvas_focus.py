
def test_canvas_focus():
    import tkinter as tk
    import matplotlib.pyplot as plt
    success = []

    def check_focus():
        tkcanvas = fig.canvas.get_tk_widget()
        # Give the plot window time to appear
        if not tkcanvas.winfo_viewable():
            tkcanvas.wait_visibility()
        # Make sure the canvas has the focus, so that it's able to receive
        # keyboard events.
        if tkcanvas.focus_lastfor() == tkcanvas:
            success.append(True)
        plt.close()
        root.destroy()

    root = tk.Tk()
    fig = plt.figure()
    plt.plot([1, 2, 3])
    root.after(0, plt.show)
    root.after(100, check_focus)
    root.mainloop()

    if success:
        print("success")

