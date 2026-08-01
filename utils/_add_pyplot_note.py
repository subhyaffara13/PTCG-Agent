
def _add_pyplot_note(func, wrapped_func):
    """
    Add a note to the docstring of *func* that it is a pyplot wrapper.

    The note is added to the "Notes" section of the docstring. If that does
    not exist, a "Notes" section is created. In numpydoc, the "Notes"
    section is the third last possible section, only potentially followed by
    "References" and "Examples".
    """
    if not func.__doc__:
        return  # nothing to do

    qualname = wrapped_func.__qualname__
    if qualname in _NO_PYPLOT_NOTE:
        return

    wrapped_func_is_method = True
    if "." not in qualname:
        # method qualnames are prefixed by the class and ".", e.g. "Axes.plot"
        wrapped_func_is_method = False
        link = f"{wrapped_func.__module__}.{qualname}"
    elif qualname.startswith("Axes."):  # e.g. "Axes.plot"
        link = ".axes." + qualname
    elif qualname.startswith("_AxesBase."):  # e.g. "_AxesBase.set_xlabel"
        link = ".axes.Axes" + qualname[9:]
    elif qualname.startswith("Figure."):  # e.g. "Figure.figimage"
        link = "." + qualname
    elif qualname.startswith("FigureBase."):  # e.g. "FigureBase.gca"
        link = ".Figure" + qualname[10:]
    elif qualname.startswith("FigureCanvasBase."):  # "FigureBaseCanvas.mpl_connect"
        link = "." + qualname
    else:
        raise RuntimeError(f"Wrapped method from unexpected class: {qualname}")

    if wrapped_func_is_method:
        message = f"This is the :ref:`pyplot wrapper <pyplot_interface>` for `{link}`."
    else:
        message = f"This is equivalent to `{link}`."

    # Find the correct insert position:
    # - either we already have a "Notes" section into which we can insert
    # - or we create one before the next present section. Note that in numpydoc, the
    #   "Notes" section is the third last possible section, only potentially followed
    #   by "References" and "Examples".
    # - or we append a new "Notes" section at the end.
    doc = inspect.cleandoc(func.__doc__)
    if "\nNotes\n-----" in doc:
        before, after = doc.split("\nNotes\n-----", 1)
    elif (index := doc.find("\nReferences\n----------")) != -1:
        before, after = doc[:index], doc[index:]
    elif (index := doc.find("\nExamples\n--------")) != -1:
        before, after = doc[:index], doc[index:]
    else:
        # No "Notes", "References", or "Examples" --> append to the end.
        before = doc + "\n"
        after = ""

    func.__doc__ = f"{before}\nNotes\n-----\n\n.. note::\n\n    {message}\n{after}"

