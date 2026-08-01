
def open_file(
    filename: str | os.PathLike[str],
    mode: str = "r",
    encoding: str | None = None,
    errors: str | None = "strict",
    lazy: bool = False,
    atomic: bool = False,
) -> t.IO[t.Any]:
    """Open a file, with extra behavior to handle ``'-'`` to indicate
    a standard stream, lazy open on write, and atomic write. Similar to
    the behavior of the :class:`~click.File` param type.

    If ``'-'`` is given to open ``stdout`` or ``stdin``, the stream is
    wrapped so that using it in a context manager will not close it.
    This makes it possible to use the function without accidentally
    closing a standard stream:

    .. code-block:: python

        with open_file(filename) as f:
            ...

    :param filename: The name or Path of the file to open, or ``'-'`` for
        ``stdin``/``stdout``.
    :param mode: The mode in which to open the file.
    :param encoding: The encoding to decode or encode a file opened in
        text mode.
    :param errors: The error handling mode.
    :param lazy: Wait to open the file until it is accessed. For read
        mode, the file is temporarily opened to raise access errors
        early, then closed until it is read again.
    :param atomic: Write to a temporary file and replace the given file
        on close.

    .. versionadded:: 3.0
    """
    if lazy:
        return t.cast(
            "t.IO[t.Any]", LazyFile(filename, mode, encoding, errors, atomic=atomic)
        )

    f, should_close = open_stream(filename, mode, encoding, errors, atomic=atomic)

    if not should_close:
        f = t.cast("t.IO[t.Any]", KeepOpenFile(f))

    return f


def open_file(path_arg, mode="r"):
    """Decorator to ensure clean opening and closing of files.

    Parameters
    ----------
    path_arg : string or int
        Name or index of the argument that is a path.

    mode : str
        String for opening mode.

    Returns
    -------
    _open_file : function
        Function which cleanly executes the io.

    Examples
    --------
    Decorate functions like this::

       @open_file(0, "r")
       def read_function(pathname):
           pass


       @open_file(1, "w")
       def write_function(G, pathname):
           pass


       @open_file(1, "w")
       def write_function(G, pathname="graph.dot"):
           pass


       @open_file("pathname", "w")
       def write_function(G, pathname="graph.dot"):
           pass


       @open_file("path", "w+")
       def another_function(arg, **kwargs):
           path = kwargs["path"]
           pass

    Notes
    -----
    Note that this decorator solves the problem when a path argument is
    specified as a string, but it does not handle the situation when the
    function wants to accept a default of None (and then handle it).

    Here is an example of how to handle this case::

      @open_file("path")
      def some_function(arg1, arg2, path=None):
          if path is None:
              fobj = tempfile.NamedTemporaryFile(delete=False)
          else:
              # `path` could have been a string or file object or something
              # similar. In any event, the decorator has given us a file object
              # and it will close it for us, if it should.
              fobj = path

          try:
              fobj.write("blah")
          finally:
              if path is None:
                  fobj.close()

    Normally, we'd want to use "with" to ensure that fobj gets closed.
    However, the decorator will make `path` a file object for us,
    and using "with" would undesirably close that file object.
    Instead, we use a try block, as shown above.
    When we exit the function, fobj will be closed, if it should be, by the decorator.
    """

    def _open_file(path):
        # Now we have the path_arg. There are two types of input to consider:
        #   1) string representing a path that should be opened
        #   2) an already opened file object
        if isinstance(path, str):
            ext = splitext(path)[1]
        elif isinstance(path, Path):
            # path is a pathlib reference to a filename
            ext = path.suffix
            path = str(path)
        else:
            # could be None, or a file handle, in which case the algorithm will deal with it
            return path, lambda: None

        fobj = _dispatch_dict[ext](path, mode=mode)
        return fobj, lambda: fobj.close()

    return argmap(_open_file, path_arg, try_finally=True)

