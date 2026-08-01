
def plot(
    *args: float | ArrayLike | str,
    scalex: bool = True,
    scaley: bool = True,
    data: DataParamType = None,
    **kwargs,
) -> list[Line2D]:
    return gca().plot(
        *args,
        scalex=scalex,
        scaley=scaley,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )


def plot(ctx, f, xlim=[-5,5], ylim=None, points=200, file=None, dpi=None,
    singularities=[], axes=None):
    r"""
    Shows a simple 2D plot of a function `f(x)` or list of functions
    `[f_0(x), f_1(x), \ldots, f_n(x)]` over a given interval
    specified by *xlim*. Some examples::

        plot(lambda x: exp(x)*li(x), [1, 4])
        plot([cos, sin], [-4, 4])
        plot([fresnels, fresnelc], [-4, 4])
        plot([sqrt, cbrt], [-4, 4])
        plot(lambda t: zeta(0.5+t*j), [-20, 20])
        plot([floor, ceil, abs, sign], [-5, 5])

    Points where the function raises a numerical exception or
    returns an infinite value are removed from the graph.
    Singularities can also be excluded explicitly
    as follows (useful for removing erroneous vertical lines)::

        plot(cot, ylim=[-5, 5])   # bad
        plot(cot, ylim=[-5, 5], singularities=[-pi, 0, pi])  # good

    For parts where the function assumes complex values, the
    real part is plotted with dashes and the imaginary part
    is plotted with dots.

    .. note :: This function requires matplotlib (pylab).
    """
    if file:
        axes = None
    fig = None
    if not axes:
        import pylab
        fig = pylab.figure()
        axes = fig.add_subplot(111)
    if not isinstance(f, (tuple, list)):
        f = [f]
    a, b = xlim
    colors = ['b', 'r', 'g', 'm', 'k']
    for n, func in enumerate(f):
        x = ctx.arange(a, b, (b-a)/float(points))
        segments = []
        segment = []
        in_complex = False
        for i in xrange(len(x)):
            try:
                if i != 0:
                    for sing in singularities:
                        if x[i-1] <= sing and x[i] >= sing:
                            raise ValueError
                v = func(x[i])
                if ctx.isnan(v) or abs(v) > 1e300:
                    raise ValueError
                if hasattr(v, "imag") and v.imag:
                    re = float(v.real)
                    im = float(v.imag)
                    if not in_complex:
                        in_complex = True
                        segments.append(segment)
                        segment = []
                    segment.append((float(x[i]), re, im))
                else:
                    if in_complex:
                        in_complex = False
                        segments.append(segment)
                        segment = []
                    if hasattr(v, "real"):
                        v = v.real
                    segment.append((float(x[i]), v))
            except ctx.plot_ignore:
                if segment:
                    segments.append(segment)
                segment = []
        if segment:
            segments.append(segment)
        for segment in segments:
            x = [s[0] for s in segment]
            y = [s[1] for s in segment]
            if not x:
                continue
            c = colors[n % len(colors)]
            if len(segment[0]) == 3:
                z = [s[2] for s in segment]
                axes.plot(x, y, '--'+c, linewidth=3)
                axes.plot(x, z, ':'+c, linewidth=3)
            else:
                axes.plot(x, y, c, linewidth=3)
    axes.set_xlim([float(_) for _ in xlim])
    if ylim:
        axes.set_ylim([float(_) for _ in ylim])
    axes.set_xlabel('x')
    axes.set_ylabel('f(x)')
    axes.grid(True)
    if fig:
        if file:
            pylab.savefig(file, dpi=dpi)
        else:
            pylab.show()


def plot(*args, show=True, **kwargs):
    """Plots a function of a single variable as a curve.

    Parameters
    ==========

    args :
        The first argument is the expression representing the function
        of single variable to be plotted.

        The last argument is a 3-tuple denoting the range of the free
        variable. e.g. ``(x, 0, 5)``

        Typical usage examples are in the following:

        - Plotting a single expression with a single range.
            ``plot(expr, range, **kwargs)``
        - Plotting a single expression with the default range (-10, 10).
            ``plot(expr, **kwargs)``
        - Plotting multiple expressions with a single range.
            ``plot(expr1, expr2, ..., range, **kwargs)``
        - Plotting multiple expressions with multiple ranges.
            ``plot((expr1, range1), (expr2, range2), ..., **kwargs)``

        It is best practice to specify range explicitly because default
        range may change in the future if a more advanced default range
        detection algorithm is implemented.

    show : bool, optional
        The default value is set to ``True``. Set show to ``False`` and
        the function will not display the plot. The returned instance of
        the ``Plot`` class can then be used to save or display the plot
        by calling the ``save()`` and ``show()`` methods respectively.

    line_color : string, or float, or function, optional
        Specifies the color for the plot.
        See ``Plot`` to see how to set color for the plots.
        Note that by setting ``line_color``, it would be applied simultaneously
        to all the series.

    title : str, optional
        Title of the plot. It is set to the latex representation of
        the expression, if the plot has only one expression.

    label : str, optional
        The label of the expression in the plot. It will be used when
        called with ``legend``. Default is the name of the expression.
        e.g. ``sin(x)``

    xlabel : str or expression, optional
        Label for the x-axis.

    ylabel : str or expression, optional
        Label for the y-axis.

    xscale : 'linear' or 'log', optional
        Sets the scaling of the x-axis.

    yscale : 'linear' or 'log', optional
        Sets the scaling of the y-axis.

    axis_center : (float, float), optional
        Tuple of two floats denoting the coordinates of the center or
        {'center', 'auto'}

    xlim : (float, float), optional
        Denotes the x-axis limits, ``(min, max)```.

    ylim : (float, float), optional
        Denotes the y-axis limits, ``(min, max)```.

    annotations : list, optional
        A list of dictionaries specifying the type of annotation
        required. The keys in the dictionary should be equivalent
        to the arguments of the :external:mod:`matplotlib`'s
        :external:meth:`~matplotlib.axes.Axes.annotate` method.

    markers : list, optional
        A list of dictionaries specifying the type the markers required.
        The keys in the dictionary should be equivalent to the arguments
        of the :external:mod:`matplotlib`'s :external:func:`~matplotlib.pyplot.plot()` function
        along with the marker related keyworded arguments.

    rectangles : list, optional
        A list of dictionaries specifying the dimensions of the
        rectangles to be plotted. The keys in the dictionary should be
        equivalent to the arguments of the :external:mod:`matplotlib`'s
        :external:class:`~matplotlib.patches.Rectangle` class.

    fill : dict, optional
        A dictionary specifying the type of color filling required in
        the plot. The keys in the dictionary should be equivalent to the
        arguments of the :external:mod:`matplotlib`'s
        :external:meth:`~matplotlib.axes.Axes.fill_between` method.

    adaptive : bool, optional
        The default value for the ``adaptive`` parameter is now ``False``.
        To enable adaptive sampling, set ``adaptive=True`` and specify ``n`` if uniform sampling is required.

        The plotting uses an adaptive algorithm which samples
        recursively to accurately plot. The adaptive algorithm uses a
        random point near the midpoint of two points that has to be
        further sampled. Hence the same plots can appear slightly
        different.

    depth : int, optional
        Recursion depth of the adaptive algorithm. A depth of value
        `n` samples a maximum of `2^{n}` points.

        If the ``adaptive`` flag is set to ``False``, this will be
        ignored.

    n : int, optional
        Used when the ``adaptive`` is set to ``False``. The function
        is uniformly sampled at ``n`` number of points. If the ``adaptive``
        flag is set to ``True``, this will be ignored.
        This keyword argument replaces ``nb_of_points``, which should be
        considered deprecated.

    size : (float, float), optional
        A tuple in the form (width, height) in inches to specify the size of
        the overall figure. The default value is set to ``None``, meaning
        the size will be set by the default backend.

    Examples
    ========

    .. plot::
       :context: close-figs
       :format: doctest
       :include-source: True

       >>> from sympy import symbols
       >>> from sympy.plotting import plot
       >>> x = symbols('x')

    Single Plot

    .. plot::
       :context: close-figs
       :format: doctest
       :include-source: True

       >>> plot(x**2, (x, -5, 5))
       Plot object containing:
       [0]: cartesian line: x**2 for x over (-5.0, 5.0)

    Multiple plots with single range.

    .. plot::
       :context: close-figs
       :format: doctest
       :include-source: True

       >>> plot(x, x**2, x**3, (x, -5, 5))
       Plot object containing:
       [0]: cartesian line: x for x over (-5.0, 5.0)
       [1]: cartesian line: x**2 for x over (-5.0, 5.0)
       [2]: cartesian line: x**3 for x over (-5.0, 5.0)

    Multiple plots with different ranges.

    .. plot::
       :context: close-figs
       :format: doctest
       :include-source: True

       >>> plot((x**2, (x, -6, 6)), (x, (x, -5, 5)))
       Plot object containing:
       [0]: cartesian line: x**2 for x over (-6.0, 6.0)
       [1]: cartesian line: x for x over (-5.0, 5.0)

    No adaptive sampling by default. If adaptive sampling is required, set ``adaptive=True``.

    .. plot::
       :context: close-figs
       :format: doctest
       :include-source: True

       >>> plot(x**2, adaptive=True, n=400)
       Plot object containing:
       [0]: cartesian line: x**2 for x over (-10.0, 10.0)

    See Also
    ========

    Plot, LineOver1DRangeSeries

    """
    args = _plot_sympify(args)
    plot_expr = _check_arguments(args, 1, 1, **kwargs)
    params = kwargs.get("params", None)
    free = set()
    for p in plot_expr:
        if not isinstance(p[1][0], str):
            free |= {p[1][0]}
        else:
            free |= {Symbol(p[1][0])}
    if params:
        free = free.difference(params.keys())
    x = free.pop() if free else Symbol("x")
    kwargs.setdefault('xlabel', x)
    kwargs.setdefault('ylabel', Function('f')(x))

    labels = kwargs.pop("label", [])
    rendering_kw = kwargs.pop("rendering_kw", None)
    series = _build_line_series(*plot_expr, **kwargs)
    _set_labels(series, labels, rendering_kw)

    plots = plot_factory(*series, **kwargs)
    if show:
        plots.show()
    return plots


def plot(data, kind, **kwargs):
    # Importing pyplot at the top of the file (before the converters are
    # registered) causes problems in matplotlib 2 (converters seem to not
    # work)
    import matplotlib.pyplot as plt

    if kwargs.pop("reuse_plot", False):
        ax = kwargs.get("ax")
        if ax is None and len(plt.get_fignums()) > 0:
            with plt.rc_context():
                ax = plt.gca()
            kwargs["ax"] = getattr(ax, "left_ax", ax)
    plot_obj = PLOT_CLASSES[kind](data, **kwargs)
    plot_obj.generate()
    plt.draw_if_interactive()
    return plot_obj.result

