
def init_session(ipython=None, pretty_print=True, order=None,
                 use_unicode=None, use_latex=None, quiet=False, auto_symbols=False,
                 auto_int_to_Integer=False, str_printer=None, pretty_printer=None,
                 latex_printer=None, argv=[]):
    """
    Initialize an embedded IPython or Python session. The IPython session is
    initiated with the --pylab option, without the numpy imports, so that
    matplotlib plotting can be interactive.

    Parameters
    ==========

    pretty_print: boolean
        If True, use pretty_print to stringify;
        if False, use sstrrepr to stringify.
    order: string or None
        There are a few different settings for this parameter:
        lex (default), which is lexographic order;
        grlex, which is graded lexographic order;
        grevlex, which is reversed graded lexographic order;
        old, which is used for compatibility reasons and for long expressions;
        None, which sets it to lex.
    use_unicode: boolean or None
        If True, use unicode characters;
        if False, do not use unicode characters.
    use_latex: boolean or None
        If True, use latex rendering if IPython GUI's;
        if False, do not use latex rendering.
    quiet: boolean
        If True, init_session will not print messages regarding its status;
        if False, init_session will print messages regarding its status.
    auto_symbols: boolean
        If True, IPython will automatically create symbols for you.
        If False, it will not.
        The default is False.
    auto_int_to_Integer: boolean
        If True, IPython will automatically wrap int literals with Integer, so
        that things like 1/2 give Rational(1, 2).
        If False, it will not.
        The default is False.
    ipython: boolean or None
        If True, printing will initialize for an IPython console;
        if False, printing will initialize for a normal console;
        The default is None, which automatically determines whether we are in
        an ipython instance or not.
    str_printer: function, optional, default=None
        A custom string printer function. This should mimic
        sympy.printing.sstrrepr().
    pretty_printer: function, optional, default=None
        A custom pretty printer. This should mimic sympy.printing.pretty().
    latex_printer: function, optional, default=None
        A custom LaTeX printer. This should mimic sympy.printing.latex()
        This should mimic sympy.printing.latex().
    argv: list of arguments for IPython
        See sympy.bin.isympy for options that can be used to initialize IPython.

    See Also
    ========

    sympy.interactive.printing.init_printing: for examples and the rest of the parameters.


    Examples
    ========

    >>> from sympy import init_session, Symbol, sin, sqrt
    >>> sin(x) #doctest: +SKIP
    NameError: name 'x' is not defined
    >>> init_session() #doctest: +SKIP
    >>> sin(x) #doctest: +SKIP
    sin(x)
    >>> sqrt(5) #doctest: +SKIP
      ___
    \\/ 5
    >>> init_session(pretty_print=False) #doctest: +SKIP
    >>> sqrt(5) #doctest: +SKIP
    sqrt(5)
    >>> y + x + y**2 + x**2 #doctest: +SKIP
    x**2 + x + y**2 + y
    >>> init_session(order='grlex') #doctest: +SKIP
    >>> y + x + y**2 + x**2 #doctest: +SKIP
    x**2 + y**2 + x + y
    >>> init_session(order='grevlex') #doctest: +SKIP
    >>> y * x**2 + x * y**2 #doctest: +SKIP
    x**2*y + x*y**2
    >>> init_session(order='old') #doctest: +SKIP
    >>> x**2 + y**2 + x + y #doctest: +SKIP
    x + y + x**2 + y**2
    >>> theta = Symbol('theta') #doctest: +SKIP
    >>> theta #doctest: +SKIP
    theta
    >>> init_session(use_unicode=True) #doctest: +SKIP
    >>> theta # doctest: +SKIP
    \u03b8
    """
    import sys

    in_ipython = False

    if ipython is not False:
        try:
            import IPython
        except ImportError:
            if ipython is True:
                raise RuntimeError("IPython is not available on this system")
            ip = None
        else:
            try:
                from IPython import get_ipython
                ip = get_ipython()
            except ImportError:
                ip = None
        in_ipython = bool(ip)
        if ipython is None:
            ipython = in_ipython

    if ipython is False:
        ip = init_python_session()
        mainloop = ip.interact
    else:
        ip = init_ipython_session(ip, argv=argv, auto_symbols=auto_symbols,
                                  auto_int_to_Integer=auto_int_to_Integer)

        if version_tuple(IPython.__version__) >= version_tuple('0.11'):
            # runsource is gone, use run_cell instead, which doesn't
            # take a symbol arg.  The second arg is `store_history`,
            # and False means don't add the line to IPython's history.
            ip.runsource = lambda src, symbol='exec': ip.run_cell(src, False)

            # Enable interactive plotting using pylab.
            try:
                ip.enable_pylab(import_all=False)
            except Exception:
                # Causes an import error if matplotlib is not installed.
                # Causes other errors (depending on the backend) if there
                # is no display, or if there is some problem in the
                # backend, so we have a bare "except Exception" here
                pass
        if not in_ipython:
            mainloop = ip.mainloop

    if auto_symbols and (not ipython or version_tuple(IPython.__version__) < version_tuple('0.11')):
        raise RuntimeError("automatic construction of symbols is possible only in IPython 0.11 or above")
    if auto_int_to_Integer and (not ipython or version_tuple(IPython.__version__) < version_tuple('0.11')):
        raise RuntimeError("automatic int to Integer transformation is possible only in IPython 0.11 or above")

    _preexec_source = preexec_source

    ip.runsource(_preexec_source, symbol='exec')
    init_printing(pretty_print=pretty_print, order=order,
                  use_unicode=use_unicode, use_latex=use_latex, ip=ip,
                  str_printer=str_printer, pretty_printer=pretty_printer,
                  latex_printer=latex_printer)

    message = _make_message(ipython, quiet, _preexec_source)

    if not in_ipython:
        print(message)
        mainloop()
        sys.exit('Exiting ...')
    else:
        print(message)
        import atexit
        atexit.register(lambda: print("Exiting ...\n"))

