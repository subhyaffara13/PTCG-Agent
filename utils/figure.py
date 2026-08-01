
def figure(
    # autoincrement if None, else integer from 1-N
    num: int | str | Figure | SubFigure | None = None,
    # defaults to rc figure.figsize
    figsize: ArrayLike  # a 2-element ndarray is accepted as well
             | tuple[float, float, Literal["in", "cm", "px"]]
             | None = None,
    # defaults to rc figure.dpi
    dpi: float | None = None,
    *,
    # defaults to rc figure.facecolor
    facecolor: ColorType | None = None,
    # defaults to rc figure.edgecolor
    edgecolor: ColorType | None = None,
    frameon: bool = True,
    FigureClass: type[Figure] = Figure,
    clear: bool = False,
    **kwargs
) -> Figure:
    """
    Create a new figure, or activate an existing figure.

    Parameters
    ----------
    num : int or str or `.Figure` or `.SubFigure`, optional
        A unique identifier for the figure.

        If a figure with that identifier already exists, this figure is made
        active and returned. An integer refers to the ``Figure.number``
        attribute, a string refers to the figure label.

        If there is no figure with the identifier or *num* is not given, a new
        figure is created, made active and returned.  If *num* is an int, it
        will be used for the ``Figure.number`` attribute, otherwise, an
        auto-generated integer value is used (starting at 1 and incremented
        for each new figure). If *num* is a string, the figure label and the
        window title is set to this value.  If num is a ``SubFigure``, its
        parent ``Figure`` is activated.

        If *num* is a Figure instance that is already tracked in pyplot, it is
        activated. If *num* is a Figure instance that is not tracked in pyplot,
        it is added to the tracked figures and activated.

    figsize : (float, float) or (float, float, str), default: :rc:`figure.figsize`
        The figure dimensions. This can be

        - a tuple ``(width, height, unit)``, where *unit* is one of "inch", "cm",
          "px".
        - a tuple ``(x, y)``, which is interpreted as ``(x, y, "inch")``.

        One of *width* or *height* may be ``None``; the respective value is taken
        from :rc:`figure.figsize`.

    dpi : float, default: :rc:`figure.dpi`
        The resolution of the figure in dots-per-inch.

    facecolor : :mpltype:`color`, default: :rc:`figure.facecolor`
        The background color.

    edgecolor : :mpltype:`color`, default: :rc:`figure.edgecolor`
        The border color.

    frameon : bool, default: True
        If False, suppress drawing the figure frame.

    FigureClass : subclass of `~matplotlib.figure.Figure`
        If set, an instance of this subclass will be created, rather than a
        plain `.Figure`.

    clear : bool, default: False
        If True and the figure already exists, then it is cleared.

    layout : {'constrained', 'compressed', 'tight', 'none', `.LayoutEngine`, None}, \
default: None
        The layout mechanism for positioning of plot elements to avoid
        overlapping Axes decorations (labels, ticks, etc). Note that layout
        managers can measurably slow down figure display.

        - 'constrained': The constrained layout solver adjusts Axes sizes
          to avoid overlapping Axes decorations.  Can handle complex plot
          layouts and colorbars, and is thus recommended.

          See :ref:`constrainedlayout_guide`
          for examples.

        - 'compressed': uses the same algorithm as 'constrained', but
          removes extra space between fixed-aspect-ratio Axes.  Best for
          simple grids of Axes.

        - 'tight': Use the tight layout mechanism. This is a relatively
          simple algorithm that adjusts the subplot parameters so that
          decorations do not overlap. See `.Figure.set_tight_layout` for
          further details.

        - 'none': Do not use a layout engine.

        - A `.LayoutEngine` instance. Builtin layout classes are
          `.ConstrainedLayoutEngine` and `.TightLayoutEngine`, more easily
          accessible by 'constrained' and 'tight'.  Passing an instance
          allows third parties to provide their own layout engine.

        If not given, fall back to using the parameters *tight_layout* and
        *constrained_layout*, including their config defaults
        :rc:`figure.autolayout` and :rc:`figure.constrained_layout.use`.

    **kwargs
        Additional keyword arguments are passed to the `.Figure` constructor.

    Returns
    -------
    `~matplotlib.figure.Figure`

    Notes
    -----
    A newly created figure is passed to the `~.FigureCanvasBase.new_manager`
    method or the `new_figure_manager` function provided by the current
    backend, which install a canvas and a manager on the figure.

    Once this is done, :rc:`figure.hooks` are called, one at a time, on the
    figure; these hooks allow arbitrary customization of the figure (e.g.,
    attaching callbacks) or of associated elements (e.g., modifying the
    toolbar).  See :doc:`/gallery/user_interfaces/mplcvd` for an example of
    toolbar customization.

    If you are creating many figures, make sure you explicitly call
    `.pyplot.close` on the figures you are not using, because this will
    enable pyplot to properly clean up the memory.

    `~matplotlib.rcParams` defines the default values, which can be modified
    in the matplotlibrc file.
    """
    allnums = get_fignums()
    next_num = max(allnums) + 1 if allnums else 1

    if isinstance(num, FigureBase):
        # type narrowed to `Figure | SubFigure` by combination of input and isinstance
        has_figure_property_parameters = (
            any(param is not None for param in [figsize, dpi, facecolor, edgecolor])
            or not frameon or kwargs
        )

        root_fig = num.get_figure(root=True)
        if root_fig.canvas.manager is None:
            if has_figure_property_parameters:
                raise ValueError(
                    "You cannot pass figure properties when calling figure() with "
                    "an existing Figure instance")
            backend = _get_backend_mod()
            manager_ = backend.new_figure_manager_given_figure(next_num, root_fig)
            _pylab_helpers.Gcf._set_new_active_manager(manager_)
            return manager_.canvas.figure
        elif has_figure_property_parameters and root_fig.canvas.manager.num in allnums:
            _api.warn_external(
                "Ignoring specified arguments in this call because figure "
                f"with num: {root_fig.canvas.manager.num} already exists")
        _pylab_helpers.Gcf.set_active(root_fig.canvas.manager)
        return root_fig

    fig_label = ''
    if num is None:
        num = next_num
    else:
        if (any(param is not None for param in [figsize, dpi, facecolor, edgecolor])
              or not frameon or kwargs) and num in allnums:
            _api.warn_external(
                "Ignoring specified arguments in this call "
                f"because figure with num: {num} already exists")
        if isinstance(num, str):
            fig_label = num
            all_labels = get_figlabels()
            if fig_label not in all_labels:
                if fig_label == 'all':
                    _api.warn_external("close('all') closes all existing figures.")
                num = next_num
            else:
                inum = all_labels.index(fig_label)
                num = allnums[inum]
        else:
            num = int(num)  # crude validation of num argument

    manager = _pylab_helpers.Gcf.get_fig_manager(num)
    if manager is None:
        max_open_warning = rcParams['figure.max_open_warning']
        if len(allnums) == max_open_warning >= 1:
            _api.warn_external(
                f"More than {max_open_warning} figures have been opened. "
                f"Figures created through the pyplot interface "
                f"(`matplotlib.pyplot.figure`) are retained until explicitly "
                f"closed and may consume too much memory. (To control this "
                f"warning, see the rcParam `figure.max_open_warning`). "
                f"Consider using `matplotlib.pyplot.close()`.",
                RuntimeWarning)

        manager = new_figure_manager(
            num, figsize=figsize, dpi=dpi,
            facecolor=facecolor, edgecolor=edgecolor, frameon=frameon,
            FigureClass=FigureClass, **kwargs)
        fig = manager.canvas.figure
        if fig_label:
            fig.set_label(fig_label)

        for hookspecs in rcParams["figure.hooks"]:
            module_name, dotted_name = hookspecs.split(":")
            obj: Any = importlib.import_module(module_name)
            for part in dotted_name.split("."):
                obj = getattr(obj, part)
            obj(fig)

        _pylab_helpers.Gcf._set_new_active_manager(manager)

        # make sure backends (inline) that we don't ship that expect this
        # to be called in plotting commands to make the figure call show
        # still work.  There is probably a better way to do this in the
        # FigureManager base class.
        draw_if_interactive()

        if _REPL_DISPLAYHOOK is _ReplDisplayHook.PLAIN:
            fig.stale_callback = _auto_draw_if_interactive

    if clear:
        manager.canvas.figure.clear()

    return manager.canvas.figure

