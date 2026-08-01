
def to_clipboard(
    obj, excel: bool | None = True, sep: str | None = None, **kwargs
) -> None:  # pragma: no cover
    """
    Attempt to write text representation of object to the system clipboard
    The clipboard can be then pasted into Excel for example.

    Parameters
    ----------
    obj : the object to write to the clipboard
    excel : bool, defaults to True
            if True, use the provided separator, writing in a csv
            format for allowing easy pasting into excel.
            if False, write a string representation of the object
            to the clipboard
    sep : optional, defaults to tab
    other keywords are passed to to_csv

    Notes
    -----
    Requirements for your platform
      - Linux: xclip, or xsel (with PyQt4 modules)
      - Windows:
      - OS X:
    """
    encoding = kwargs.pop("encoding", "utf-8")

    # testing if an invalid encoding is passed to clipboard
    if encoding is not None and encoding.lower().replace("-", "") != "utf8":
        raise ValueError("clipboard only supports utf-8 encoding")

    from pandas.io.clipboard import clipboard_set

    if excel is None:
        excel = True

    if excel:
        try:
            if sep is None:
                sep = "\t"
            buf = StringIO()

            # clipboard_set (pyperclip) expects unicode
            obj.to_csv(buf, sep=sep, encoding="utf-8", **kwargs)
            text = buf.getvalue()

            clipboard_set(text)
            return
        except TypeError:
            warnings.warn(
                "to_clipboard in excel mode requires a single character separator.",
                stacklevel=find_stack_level(),
            )
    elif sep is not None:
        warnings.warn(
            "to_clipboard with excel=False ignores the sep argument.",
            stacklevel=find_stack_level(),
        )

    if isinstance(obj, ABCDataFrame):
        # str(df) has various unhelpful defaults, like truncation
        with option_context("display.max_colwidth", None):
            objstr = obj.to_string(**kwargs)
    else:
        objstr = str(obj)
    clipboard_set(objstr)

