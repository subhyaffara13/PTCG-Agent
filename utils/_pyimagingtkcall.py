
def _pyimagingtkcall(
    command: str, photo: PhotoImage | tkinter.PhotoImage, ptr: CapsuleType
) -> None:
    tk = photo.tk
    try:
        tk.call(command, photo, repr(ptr))
    except tkinter.TclError:
        # activate Tkinter hook
        # may raise an error if it cannot attach to Tkinter
        from . import _imagingtk

        _imagingtk.tkinit(tk.interpaddr())
        tk.call(command, photo, repr(ptr))

