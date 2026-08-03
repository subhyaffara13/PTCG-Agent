from typing import Any

def show(*, block: bool, **kwargs) -> None: ...


def show(*args: Any, **kwargs: Any) -> None: ...


def show(*args, **kwargs) -> None:
    """
    Display all open figures.

    Parameters
    ----------
    block : bool, optional
        Whether to wait for all figures to be closed before returning.

        If `True` block and run the GUI main loop until all figure windows
        are closed.

        If `False` ensure that all figure windows are displayed and return
        immediately.  In this case, you are responsible for ensuring
        that the event loop is running to have responsive figures.

        Defaults to True in non-interactive mode and to False in interactive
        mode (see `.pyplot.isinteractive`).

    See Also
    --------
    ion : Enable interactive mode, which shows / updates the figure after
          every plotting command, so that calling ``show()`` is not necessary.
    ioff : Disable interactive mode.
    savefig : Save the figure to an image file instead of showing it on screen.

    Notes
    -----
    **Saving figures to file and showing a window at the same time**

    If you want an image file as well as a user interface window, use
    `.pyplot.savefig` before `.pyplot.show`. At the end of (a blocking)
    ``show()`` the figure is closed and thus unregistered from pyplot. Calling
    `.pyplot.savefig` afterwards would save a new and thus empty figure. This
    limitation of command order does not apply if the show is non-blocking or
    if you keep a reference to the figure and use `.Figure.savefig`.

    **Auto-show in jupyter notebooks**

    The jupyter backends (activated via ``%matplotlib inline``,
    ``%matplotlib notebook``, or ``%matplotlib widget``), call ``show()`` at
    the end of every cell by default. Thus, you usually don't have to call it
    explicitly there.
    """
    _warn_if_gui_out_of_main_thread()
    return _get_backend_mod().show(*args, **kwargs)


def show(mode=DisplayModes.stdout.value):
    """
    Show libraries and system information on which NumPy was built
    and is being used

    Parameters
    ----------
    mode : {`'stdout'`, `'dicts'`}, optional.
        Indicates how to display the config information.
        `'stdout'` prints to console, `'dicts'` returns a dictionary
        of the configuration.

    Returns
    -------
    out : {`dict`, `None`}
        If mode is `'dicts'`, a dict is returned, else None

    See Also
    --------
    get_include : Returns the directory containing NumPy C
                  header files.

    Notes
    -----
    1. The `'stdout'` mode will give more readable
       output if ``pyyaml`` is installed

    """
    if mode == DisplayModes.stdout.value:
        try:  # Non-standard library, check import
            yaml = _check_pyyaml()

            print(yaml.dump(CONFIG))
        except ModuleNotFoundError:
            import warnings
            import json

            warnings.warn("Install `pyyaml` for better output", stacklevel=1)
            print(json.dumps(CONFIG, indent=2))
    elif mode == DisplayModes.dicts.value:
        return CONFIG
    else:
        raise AttributeError(
            f"Invalid `mode`, use one of: {', '.join([e.value for e in DisplayModes])}"
        )


def show(image: Image.Image, title: str | None = None, **options: Any) -> bool:
    r"""
    Display a given image.

    :param image: An image object.
    :param title: Optional title. Not all viewers can display the title.
    :param \**options: Additional viewer options.
    :returns: ``True`` if a suitable viewer was found, ``False`` otherwise.
    """
    for viewer in _viewers:
        if viewer.show(image, title=title, **options):
            return True
    return False


def show(mode=DisplayModes.stdout.value):
    """
    Show libraries and system information on which SciPy was built
    and is being used

    Parameters
    ----------
    mode : {`'stdout'`, `'dicts'`}, optional.
        Indicates how to display the config information.
        `'stdout'` prints to console, `'dicts'` returns a dictionary
        of the configuration.

    Returns
    -------
    out : {`dict`, `None`}
        If mode is `'dicts'`, a dict is returned, else None

    Examples
    --------
    >>> import scipy
    >>> scipy.show_config()
    ... # formatted output is printed to the console

    >>> config_dict = scipy.show_config(mode='dicts')
    >>> list(config_dict.keys())
    ['Compilers', 'Machine Information', 'Build Dependencies', 'Python Information']

    Notes
    -----
    1. The `'stdout'` mode will give more readable
       output if ``pyyaml`` is installed

    """
    if mode == DisplayModes.stdout.value:
        try:  # Non-standard library, check import
            yaml = _check_pyyaml()

            print(yaml.dump(CONFIG))
        except ModuleNotFoundError:
            import warnings
            import json

            warnings.warn("Install `pyyaml` for better output", stacklevel=1)
            print(json.dumps(CONFIG, indent=2))
    elif mode == DisplayModes.dicts.value:
        return CONFIG
    else:
        raise AttributeError(
            f"Invalid `mode`, use one of: {', '.join([e.value for e in DisplayModes])}"
        )


def show() -> str:
    """
    Return a human-readable string with descriptions of the
    configuration of PyTorch.
    """
    return torch._C._show_config()


def show(
    *args,
    wrap: bool = False,
    space_separated: bool = True,
    autovisualize: bool | autovisualize_lib.Autovisualizer | None = None,
):
  """Shows a list of objects inline, like python print, but with rich display.

  Args:
    *args: Values to show. Strings show as themselves, like python's print.
      Anything renderable by Treescope will show as it's treescope
      representation. Anything with a rich IPython representation will show as
      its IPython representation.
    wrap: Whether to wrap at the end of the line.
    space_separated: Whether to add single spaces between objects.
    autovisualize: Optional autovisualizer override. If True, renders using the
      default autovisualizer (usually an array autovisualizer). If False,
      disables automatic visualization. If a function or object, uses that
      autovisualizer. If None (the default), uses the current active
      autovisualizer (if any) without overriding it.

  Raises:
    RuntimeError: If IPython is not available.
  """
  if IPython is None:
    raise RuntimeError("Cannot use `show` outside of IPython.")
  if space_separated and args:
    separated_args = []
    for arg in args:
      separated_args.append(arg)
      separated_args.append(" ")
    args = separated_args[:-1]
  with contextlib.ExitStack() as stack:
    if autovisualize is not None:
      if autovisualize is True:  # pylint: disable=g-bool-id-comparison
        tmp_autovisualizer = default_magic_autovisualizer.get()
      elif autovisualize is False:  # pylint: disable=g-bool-id-comparison
        tmp_autovisualizer = None
      else:
        tmp_autovisualizer = autovisualize
      stack.enter_context(
          autovisualize_lib.active_autovisualizer.set_scoped(tmp_autovisualizer)
      )
    IPython.display.display(figures.inline(*args, wrap=wrap))


def show(image):
    screen = pg.display.get_surface()
    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))
    pg.display.flip()
    while True:
        event = pg.event.wait()
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type in [pg.MOUSEBUTTONDOWN, pg.KEYDOWN]:
            break


def show(*objs, **kwargs) -> None:
  """Alias for `IPython.display.display`."""
  IPython.display.display(*objs, **kwargs)

