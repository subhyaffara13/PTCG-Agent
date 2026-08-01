
def init_printing(pretty_print=True, order=None, use_unicode=None,
                  use_latex=None, wrap_line=None, num_columns=None,
                  no_global=False, ip=None, euler=False, forecolor=None,
                  backcolor='Transparent', fontsize='10pt',
                  latex_mode='plain', print_builtin=True,
                  str_printer=None, pretty_printer=None,
                  latex_printer=None, scale=1.0, **settings):
    r"""
    Initializes pretty-printer depending on the environment.

    Parameters
    ==========

    pretty_print : bool, default=True
        If ``True``, use :func:`~.pretty_print` to stringify or the provided pretty
        printer; if ``False``, use :func:`~.sstrrepr` to stringify or the provided string
        printer.
    order : string or None, default='lex'
        There are a few different settings for this parameter:
        ``'lex'`` (default), which is lexographic order;
        ``'grlex'``, which is graded lexographic order;
        ``'grevlex'``, which is reversed graded lexographic order;
        ``'old'``, which is used for compatibility reasons and for long expressions;
        ``None``, which sets it to lex.
    use_unicode : bool or None, default=None
        If ``True``, use unicode characters;
        if ``False``, do not use unicode characters;
        if ``None``, make a guess based on the environment.
    use_latex : string, bool, or None, default=None
        If ``True``, use default LaTeX rendering in GUI interfaces (png and
        mathjax);
        if ``False``, do not use LaTeX rendering;
        if ``None``, make a guess based on the environment;
        if ``'png'``, enable LaTeX rendering with an external LaTeX compiler,
        falling back to matplotlib if external compilation fails;
        if ``'matplotlib'``, enable LaTeX rendering with matplotlib;
        if ``'mathjax'``, enable LaTeX text generation, for example MathJax
        rendering in IPython notebook or text rendering in LaTeX documents;
        if ``'svg'``, enable LaTeX rendering with an external latex compiler,
        no fallback
    wrap_line : bool
        If True, lines will wrap at the end; if False, they will not wrap
        but continue as one line. This is only relevant if ``pretty_print`` is
        True.
    num_columns : int or None, default=None
        If ``int``, number of columns before wrapping is set to num_columns; if
        ``None``, number of columns before wrapping is set to terminal width.
        This is only relevant if ``pretty_print`` is ``True``.
    no_global : bool, default=False
        If ``True``, the settings become system wide;
        if ``False``, use just for this console/session.
    ip : An interactive console
        This can either be an instance of IPython,
        or a class that derives from code.InteractiveConsole.
    euler : bool, optional, default=False
        Loads the euler package in the LaTeX preamble for handwritten style
        fonts (https://www.ctan.org/pkg/euler).
    forecolor : string or None, optional, default=None
        DVI setting for foreground color. ``None`` means that either ``'Black'``,
        ``'White'``, or ``'Gray'`` will be selected based on a guess of the IPython
        terminal color setting. See notes.
    backcolor : string, optional, default='Transparent'
        DVI setting for background color. See notes.
    fontsize : string or int, optional, default='10pt'
        A font size to pass to the LaTeX documentclass function in the
        preamble. Note that the options are limited by the documentclass.
        Consider using scale instead.
    latex_mode : string, optional, default='plain'
        The mode used in the LaTeX printer. Can be one of:
        ``{'inline'|'plain'|'equation'|'equation*'}``.
    print_builtin : boolean, optional, default=True
        If ``True`` then floats and integers will be printed. If ``False`` the
        printer will only print SymPy types.
    str_printer : function, optional, default=None
        A custom string printer function. This should mimic
        :func:`~.sstrrepr`.
    pretty_printer : function, optional, default=None
        A custom pretty printer. This should mimic :func:`~.pretty`.
    latex_printer : function, optional, default=None
        A custom LaTeX printer. This should mimic :func:`~.latex`.
    scale : float, optional, default=1.0
        Scale the LaTeX output when using the ``'png'`` or ``'svg'`` backends.
        Useful for high dpi screens.
    settings :
        Any additional settings for the ``latex`` and ``pretty`` commands can
        be used to fine-tune the output.

    Examples
    ========

    >>> from sympy.interactive import init_printing
    >>> from sympy import Symbol, sqrt
    >>> from sympy.abc import x, y
    >>> sqrt(5)
    sqrt(5)
    >>> init_printing(pretty_print=True) # doctest: +SKIP
    >>> sqrt(5) # doctest: +SKIP
      ___
    \/ 5
    >>> theta = Symbol('theta') # doctest: +SKIP
    >>> init_printing(use_unicode=True) # doctest: +SKIP
    >>> theta # doctest: +SKIP
    \u03b8
    >>> init_printing(use_unicode=False) # doctest: +SKIP
    >>> theta # doctest: +SKIP
    theta
    >>> init_printing(order='lex') # doctest: +SKIP
    >>> str(y + x + y**2 + x**2) # doctest: +SKIP
    x**2 + x + y**2 + y
    >>> init_printing(order='grlex') # doctest: +SKIP
    >>> str(y + x + y**2 + x**2) # doctest: +SKIP
    x**2 + x + y**2 + y
    >>> init_printing(order='grevlex') # doctest: +SKIP
    >>> str(y * x**2 + x * y**2) # doctest: +SKIP
    x**2*y + x*y**2
    >>> init_printing(order='old') # doctest: +SKIP
    >>> str(x**2 + y**2 + x + y) # doctest: +SKIP
    x**2 + x + y**2 + y
    >>> init_printing(num_columns=10) # doctest: +SKIP
    >>> x**2 + x + y**2 + y # doctest: +SKIP
    x + y +
    x**2 + y**2

    Notes
    =====

    The foreground and background colors can be selected when using ``'png'`` or
    ``'svg'`` LaTeX rendering. Note that before the ``init_printing`` command is
    executed, the LaTeX rendering is handled by the IPython console and not SymPy.

    The colors can be selected among the 68 standard colors known to ``dvips``,
    for a list see [1]_. In addition, the background color can be
    set to  ``'Transparent'`` (which is the default value).

    When using the ``'Auto'`` foreground color, the guess is based on the
    ``colors`` variable in the IPython console, see [2]_. Hence, if
    that variable is set correctly in your IPython console, there is a high
    chance that the output will be readable, although manual settings may be
    needed.


    References
    ==========

    .. [1] https://en.wikibooks.org/wiki/LaTeX/Colors#The_68_standard_colors_known_to_dvips

    .. [2] https://ipython.readthedocs.io/en/stable/config/details.html#terminal-colors

    See Also
    ========

    sympy.printing.latex
    sympy.printing.pretty

    """
    import sys
    from sympy.printing.printer import Printer

    if pretty_print:
        if pretty_printer is not None:
            stringify_func = pretty_printer
        else:
            from sympy.printing import pretty as stringify_func
    else:
        if str_printer is not None:
            stringify_func = str_printer
        else:
            from sympy.printing import sstrrepr as stringify_func

    # Even if ip is not passed, double check that not in IPython shell
    in_ipython = False
    if ip is None:
        try:
            ip = get_ipython()
        except NameError:
            pass
        else:
            in_ipython = (ip is not None)

    if ip and not in_ipython:
        in_ipython = _is_ipython(ip)

    if in_ipython and pretty_print:
        try:
            from IPython.terminal.interactiveshell import TerminalInteractiveShell
            from code import InteractiveConsole
        except ImportError:
            pass
        else:
            # This will be True if we are in the qtconsole or notebook
            if not isinstance(ip, (InteractiveConsole, TerminalInteractiveShell)) \
                    and 'ipython-console' not in ''.join(sys.argv):
                if use_unicode is None:
                    debug("init_printing: Setting use_unicode to True")
                    use_unicode = True
                if use_latex is None:
                    debug("init_printing: Setting use_latex to True")
                    use_latex = True

    if not NO_GLOBAL and not no_global:
        Printer.set_global_settings(order=order, use_unicode=use_unicode,
                                    wrap_line=wrap_line, num_columns=num_columns)
    else:
        _stringify_func = stringify_func

        if pretty_print:
            stringify_func = lambda expr, **settings: \
                             _stringify_func(expr, order=order,
                                             use_unicode=use_unicode,
                                             wrap_line=wrap_line,
                                             num_columns=num_columns,
                                             **settings)
        else:
            stringify_func = \
                lambda expr, **settings: _stringify_func(
                    expr, order=order, **settings)

    if in_ipython:
        mode_in_settings = settings.pop("mode", None)
        if mode_in_settings:
            debug("init_printing: Mode is not able to be set due to internals"
                  "of IPython printing")
        _init_ipython_printing(ip, stringify_func, use_latex, euler,
                               forecolor, backcolor, fontsize, latex_mode,
                               print_builtin, latex_printer, scale,
                               **settings)
    else:
        _init_python_printing(stringify_func, **settings)

