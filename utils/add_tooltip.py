
def add_tooltip(widget, text):
    tipwindow = None

    def showtip(event):
        """Display text in tooltip window."""
        nonlocal tipwindow
        if tipwindow or not text:
            return
        x, y, _, _ = widget.bbox("insert")
        x = x + widget.winfo_rootx() + widget.winfo_width()
        y = y + widget.winfo_rooty()
        tipwindow = tk.Toplevel(widget)
        tipwindow.overrideredirect(1)
        tipwindow.geometry(f"+{x}+{y}")
        try:  # For Mac OS
            tipwindow.tk.call("::tk::unsupported::MacWindowStyle",
                              "style", tipwindow._w,
                              "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tipwindow, text=text, justify=tk.LEFT,
                         relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hidetip(event):
        nonlocal tipwindow
        if tipwindow:
            tipwindow.destroy()
        tipwindow = None

    widget.bind("<Enter>", showtip)
    widget.bind("<Leave>", hidetip)

