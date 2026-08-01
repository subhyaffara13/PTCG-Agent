
def latex(expr, **settings):
    r"""Convert the given expression to LaTeX string representation.

    Parameters
    ==========
    full_prec: boolean, optional
        If set to True, a floating point number is printed with full precision.
    fold_frac_powers : boolean, optional
        Emit ``^{p/q}`` instead of ``^{\frac{p}{q}}`` for fractional powers.
    fold_func_brackets : boolean, optional
        Fold function brackets where applicable.
    fold_short_frac : boolean, optional
        Emit ``p / q`` instead of ``\frac{p}{q}`` when the denominator is
        simple enough (at most two terms and no powers). The default value is
        ``True`` for inline mode, ``False`` otherwise.
    inv_trig_style : string, optional
        How inverse trig functions should be displayed. Can be one of
        ``'abbreviated'``, ``'full'``, or ``'power'``. Defaults to
        ``'abbreviated'``.
    itex : boolean, optional
        Specifies if itex-specific syntax is used, including emitting
        ``$$...$$``.
    ln_notation : boolean, optional
        If set to ``True``, ``\ln`` is used instead of default ``\log``.
    long_frac_ratio : float or None, optional
        The allowed ratio of the width of the numerator to the width of the
        denominator before the printer breaks off long fractions. If ``None``
        (the default value), long fractions are not broken up.
    mat_delim : string, optional
        The delimiter to wrap around matrices. Can be one of ``'['``, ``'('``,
        or the empty string ``''``. Defaults to ``'['``.
    mat_str : string, optional
        Which matrix environment string to emit. ``'smallmatrix'``,
        ``'matrix'``, ``'array'``, etc. Defaults to ``'smallmatrix'`` for
        inline mode, ``'matrix'`` for matrices of no more than 10 columns, and
        ``'array'`` otherwise.
    mode: string, optional
        Specifies how the generated code will be delimited. ``mode`` can be one
        of ``'plain'``, ``'inline'``, ``'equation'`` or ``'equation*'``.  If
        ``mode`` is set to ``'plain'``, then the resulting code will not be
        delimited at all (this is the default). If ``mode`` is set to
        ``'inline'`` then inline LaTeX ``$...$`` will be used. If ``mode`` is
        set to ``'equation'`` or ``'equation*'``, the resulting code will be
        enclosed in the ``equation`` or ``equation*`` environment (remember to
        import ``amsmath`` for ``equation*``), unless the ``itex`` option is
        set. In the latter case, the ``$$...$$`` syntax is used.
    mul_symbol : string or None, optional
        The symbol to use for multiplication. Can be one of ``None``,
        ``'ldot'``, ``'dot'``, or ``'times'``.
    order: string, optional
        Any of the supported monomial orderings (currently ``'lex'``,
        ``'grlex'``, or ``'grevlex'``), ``'old'``, and ``'none'``. This
        parameter does nothing for `~.Mul` objects. Setting order to ``'old'``
        uses the compatibility ordering for ``~.Add`` defined in Printer. For
        very large expressions, set the ``order`` keyword to ``'none'`` if
        speed is a concern.
    symbol_names : dictionary of strings mapped to symbols, optional
        Dictionary of symbols and the custom strings they should be emitted as.
    root_notation : boolean, optional
        If set to ``False``, exponents of the form 1/n are printed in fractonal
        form. Default is ``True``, to print exponent in root form.
    mat_symbol_style : string, optional
        Can be either ``'plain'`` (default) or ``'bold'``. If set to
        ``'bold'``, a `~.MatrixSymbol` A will be printed as ``\mathbf{A}``,
        otherwise as ``A``.
    imaginary_unit : string, optional
        String to use for the imaginary unit. Defined options are ``'i'``
        (default) and ``'j'``. Adding ``r`` or ``t`` in front gives ``\mathrm``
        or ``\text``, so ``'ri'`` leads to ``\mathrm{i}`` which gives
        `\mathrm{i}`.
    gothic_re_im : boolean, optional
        If set to ``True``, `\Re` and `\Im` is used for ``re`` and ``im``, respectively.
        The default is ``False`` leading to `\operatorname{re}` and `\operatorname{im}`.
    decimal_separator : string, optional
        Specifies what separator to use to separate the whole and fractional parts of a
        floating point number as in `2.5` for the default, ``period`` or `2{,}5`
        when ``comma`` is specified. Lists, sets, and tuple are printed with semicolon
        separating the elements when ``comma`` is chosen. For example, [1; 2; 3] when
        ``comma`` is chosen and [1,2,3] for when ``period`` is chosen.
    parenthesize_super : boolean, optional
        If set to ``False``, superscripted expressions will not be parenthesized when
        powered. Default is ``True``, which parenthesizes the expression when powered.
    min: Integer or None, optional
        Sets the lower bound for the exponent to print floating point numbers in
        fixed-point format.
    max: Integer or None, optional
        Sets the upper bound for the exponent to print floating point numbers in
        fixed-point format.
    diff_operator: string, optional
        String to use for differential operator. Default is ``'d'``, to print in italic
        form. ``'rd'``, ``'td'`` are shortcuts for ``\mathrm{d}`` and ``\text{d}``.
    adjoint_style: string, optional
        String to use for the adjoint symbol. Defined options are ``'dagger'``
        (default),``'star'``, and ``'hermitian'``.

    Notes
    =====

    Not using a print statement for printing, results in double backslashes for
    latex commands since that's the way Python escapes backslashes in strings.

    >>> from sympy import latex, Rational
    >>> from sympy.abc import tau
    >>> latex((2*tau)**Rational(7,2))
    '8 \\sqrt{2} \\tau^{\\frac{7}{2}}'
    >>> print(latex((2*tau)**Rational(7,2)))
    8 \sqrt{2} \tau^{\frac{7}{2}}

    Examples
    ========

    >>> from sympy import latex, pi, sin, asin, Integral, Matrix, Rational, log
    >>> from sympy.abc import x, y, mu, r, tau

    Basic usage:

    >>> print(latex((2*tau)**Rational(7,2)))
    8 \sqrt{2} \tau^{\frac{7}{2}}

    ``mode`` and ``itex`` options:

    >>> print(latex((2*mu)**Rational(7,2), mode='plain'))
    8 \sqrt{2} \mu^{\frac{7}{2}}
    >>> print(latex((2*tau)**Rational(7,2), mode='inline'))
    $8 \sqrt{2} \tau^{7 / 2}$
    >>> print(latex((2*mu)**Rational(7,2), mode='equation*'))
    \begin{equation*}8 \sqrt{2} \mu^{\frac{7}{2}}\end{equation*}
    >>> print(latex((2*mu)**Rational(7,2), mode='equation'))
    \begin{equation}8 \sqrt{2} \mu^{\frac{7}{2}}\end{equation}
    >>> print(latex((2*mu)**Rational(7,2), mode='equation', itex=True))
    $$8 \sqrt{2} \mu^{\frac{7}{2}}$$
    >>> print(latex((2*mu)**Rational(7,2), mode='plain'))
    8 \sqrt{2} \mu^{\frac{7}{2}}
    >>> print(latex((2*tau)**Rational(7,2), mode='inline'))
    $8 \sqrt{2} \tau^{7 / 2}$
    >>> print(latex((2*mu)**Rational(7,2), mode='equation*'))
    \begin{equation*}8 \sqrt{2} \mu^{\frac{7}{2}}\end{equation*}
    >>> print(latex((2*mu)**Rational(7,2), mode='equation'))
    \begin{equation}8 \sqrt{2} \mu^{\frac{7}{2}}\end{equation}
    >>> print(latex((2*mu)**Rational(7,2), mode='equation', itex=True))
    $$8 \sqrt{2} \mu^{\frac{7}{2}}$$

    Fraction options:

    >>> print(latex((2*tau)**Rational(7,2), fold_frac_powers=True))
    8 \sqrt{2} \tau^{7/2}
    >>> print(latex((2*tau)**sin(Rational(7,2))))
    \left(2 \tau\right)^{\sin{\left(\frac{7}{2} \right)}}
    >>> print(latex((2*tau)**sin(Rational(7,2)), fold_func_brackets=True))
    \left(2 \tau\right)^{\sin {\frac{7}{2}}}
    >>> print(latex(3*x**2/y))
    \frac{3 x^{2}}{y}
    >>> print(latex(3*x**2/y, fold_short_frac=True))
    3 x^{2} / y
    >>> print(latex(Integral(r, r)/2/pi, long_frac_ratio=2))
    \frac{\int r\, dr}{2 \pi}
    >>> print(latex(Integral(r, r)/2/pi, long_frac_ratio=0))
    \frac{1}{2 \pi} \int r\, dr

    Multiplication options:

    >>> print(latex((2*tau)**sin(Rational(7,2)), mul_symbol="times"))
    \left(2 \times \tau\right)^{\sin{\left(\frac{7}{2} \right)}}

    Trig options:

    >>> print(latex(asin(Rational(7,2))))
    \operatorname{asin}{\left(\frac{7}{2} \right)}
    >>> print(latex(asin(Rational(7,2)), inv_trig_style="full"))
    \arcsin{\left(\frac{7}{2} \right)}
    >>> print(latex(asin(Rational(7,2)), inv_trig_style="power"))
    \sin^{-1}{\left(\frac{7}{2} \right)}

    Matrix options:

    >>> print(latex(Matrix(2, 1, [x, y])))
    \left[\begin{matrix}x\\y\end{matrix}\right]
    >>> print(latex(Matrix(2, 1, [x, y]), mat_str = "array"))
    \left[\begin{array}{c}x\\y\end{array}\right]
    >>> print(latex(Matrix(2, 1, [x, y]), mat_delim="("))
    \left(\begin{matrix}x\\y\end{matrix}\right)

    Custom printing of symbols:

    >>> print(latex(x**2, symbol_names={x: 'x_i'}))
    x_i^{2}

    Logarithms:

    >>> print(latex(log(10)))
    \log{\left(10 \right)}
    >>> print(latex(log(10), ln_notation=True))
    \ln{\left(10 \right)}

    ``latex()`` also supports the builtin container types :class:`list`,
    :class:`tuple`, and :class:`dict`:

    >>> print(latex([2/x, y], mode='inline'))
    $\left[ 2 / x, \  y\right]$

    Unsupported types are rendered as monospaced plaintext:

    >>> print(latex(int))
    \mathtt{\text{<class 'int'>}}
    >>> print(latex("plain % text"))
    \mathtt{\text{plain \% text}}

    See :ref:`printer_method_example` for an example of how to override
    this behavior for your own types by implementing ``_latex``.

    .. versionchanged:: 1.7.0
        Unsupported types no longer have their ``str`` representation treated as valid latex.

    """
    return LatexPrinter(settings).doprint(expr)

