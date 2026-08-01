
def table(
    cellText=None,
    cellColours=None,
    cellLoc="right",
    colWidths=None,
    rowLabels=None,
    rowColours=None,
    rowLoc="left",
    colLabels=None,
    colColours=None,
    colLoc="center",
    loc="bottom",
    bbox=None,
    edges="closed",
    **kwargs,
):
    return gca().table(
        cellText=cellText,
        cellColours=cellColours,
        cellLoc=cellLoc,
        colWidths=colWidths,
        rowLabels=rowLabels,
        rowColours=rowColours,
        rowLoc=rowLoc,
        colLabels=colLabels,
        colColours=colColours,
        colLoc=colLoc,
        loc=loc,
        bbox=bbox,
        edges=edges,
        **kwargs,
    )


def table(ax,
          cellText=None, cellColours=None,
          cellLoc='right', colWidths=None,
          rowLabels=None, rowColours=None, rowLoc='left',
          colLabels=None, colColours=None, colLoc='center',
          loc='bottom', bbox=None, edges='closed',
          **kwargs):
    """
    Add a table to an `~.axes.Axes`.

    .. note::

        ``table()`` has some fundamental design limitations and will not be
        developed further. If you need more functionality, consider
        `blume <https://github.com/swfiua/blume>`__.

    At least one of *cellText* or *cellColours* must be specified. These
    parameters must be 2D lists, in which the outer lists define the rows and
    the inner list define the column values per row. Each row must have the
    same number of elements.

    The table can optionally have row and column headers, which are configured
    using *rowLabels*, *rowColours*, *rowLoc* and *colLabels*, *colColours*,
    *colLoc* respectively.

    For finer grained control over tables, use the `.Table` class and add it to
    the Axes with `.Axes.add_table`.

    Parameters
    ----------
    cellText : 2D list of str or pandas.DataFrame, optional
        The texts to place into the table cells.

        *Note*: Line breaks in the strings are currently not accounted for and
        will result in the text exceeding the cell boundaries.

    cellColours : 2D list of :mpltype:`color`, optional
        The background colors of the cells.

    cellLoc : {'right', 'center', 'left'}
        The alignment of the text within the cells.

    colWidths : list of float, optional
        The column widths in units of the axes. If not given, all columns will
        have a width of *1 / ncols*.

    rowLabels : list of str, optional
        The text of the row header cells.

    rowColours : list of :mpltype:`color`, optional
        The colors of the row header cells.

    rowLoc : {'left', 'center', 'right'}
        The text alignment of the row header cells.

    colLabels : list of str, optional
        The text of the column header cells.

    colColours : list of :mpltype:`color`, optional
        The colors of the column header cells.

    colLoc : {'center', 'left', 'right'}
        The text alignment of the column header cells.

    loc : str, default: 'bottom'
        The position of the cell with respect to *ax*. This must be one of
        the `~.Table.codes`.

    bbox : `.Bbox` or [xmin, ymin, width, height], optional
        A bounding box to draw the table into. If this is not *None*, this
        overrides *loc*.

    edges : {'closed', 'open', 'horizontal', 'vertical'} or substring of 'BRTL'
        The cell edges to be drawn with a line. See also
        `~.Cell.visible_edges`.

    Returns
    -------
    `~matplotlib.table.Table`
        The created table.

    Other Parameters
    ----------------
    **kwargs
        `.Table` properties.

    %(Table:kwdoc)s
    """

    if cellColours is None and cellText is None:
        raise ValueError('At least one argument from "cellColours" or '
                         '"cellText" must be provided to create a table.')

    # Check we have some cellText
    if cellText is None:
        # assume just colours are needed
        rows = len(cellColours)
        cols = len(cellColours[0])
        cellText = [[''] * cols] * rows

    # Check if we have a Pandas DataFrame
    if _is_pandas_dataframe(cellText):
        # if rowLabels/colLabels are empty, use DataFrame entries.
        # Otherwise, throw an error.
        if rowLabels is None:
            rowLabels = cellText.index
        else:
            raise ValueError("rowLabels cannot be used alongside Pandas DataFrame")
        if colLabels is None:
            colLabels = cellText.columns
        else:
            raise ValueError("colLabels cannot be used alongside Pandas DataFrame")
        # Update cellText with only values
        cellText = cellText.values

    rows = len(cellText)
    cols = len(cellText[0])
    for row in cellText:
        if len(row) != cols:
            raise ValueError(f"Each row in 'cellText' must have {cols} "
                             "columns")

    if cellColours is not None:
        if len(cellColours) != rows:
            raise ValueError(f"'cellColours' must have {rows} rows")
        for row in cellColours:
            if len(row) != cols:
                raise ValueError("Each row in 'cellColours' must have "
                                 f"{cols} columns")
    else:
        cellColours = ['w' * cols] * rows

    # Set colwidths if not given
    if colWidths is None:
        colWidths = [1.0 / cols] * cols

    # Fill in missing information for column
    # and row labels
    rowLabelWidth = 0
    if rowLabels is None:
        if rowColours is not None:
            rowLabels = [''] * rows
            rowLabelWidth = colWidths[0]
    elif rowColours is None:
        rowColours = 'w' * rows

    if rowLabels is not None:
        if len(rowLabels) != rows:
            raise ValueError(f"'rowLabels' must be of length {rows}")

    # If we have column labels, need to shift
    # the text and colour arrays down 1 row
    offset = 1
    if colLabels is None:
        if colColours is not None:
            colLabels = [''] * cols
        else:
            offset = 0
    elif colColours is None:
        colColours = 'w' * cols

    # Set up cell colours if not given
    if cellColours is None:
        cellColours = ['w' * cols] * rows

    # Now create the table
    table = Table(ax, loc, bbox, **kwargs)
    table.edges = edges
    height = table._approx_text_height()

    # Add the cells
    for row in range(rows):
        for col in range(cols):
            table.add_cell(row + offset, col,
                           width=colWidths[col], height=height,
                           text=cellText[row][col],
                           facecolor=cellColours[row][col],
                           loc=cellLoc)
    # Do column labels
    if colLabels is not None:
        for col in range(cols):
            table.add_cell(0, col,
                           width=colWidths[col], height=height,
                           text=colLabels[col], facecolor=colColours[col],
                           loc=colLoc)

    # Do row labels
    if rowLabels is not None:
        for row in range(rows):
            table.add_cell(row + offset, -1,
                           width=rowLabelWidth or 1e-15, height=height,
                           text=rowLabels[row], facecolor=rowColours[row],
                           loc=rowLoc)
        if rowLabelWidth == 0:
            table.auto_set_column_width(-1)

    # set_fontsize is only effective after cells are added
    if "fontsize" in kwargs:
        table.set_fontsize(kwargs["fontsize"])

    ax.add_table(table)
    return table


def table(is_super_table: bool | None = None) -> Table:
    """Create an empty table.

    :param is_super_table: if true, the table is a super table

    :Example:

    >>> doc = document()
    >>> foo = table(True)
    >>> bar = table()
    >>> bar.update({'x': 1})
    >>> foo.append('bar', bar)
    >>> doc.append('foo', foo)
    >>> print(doc.as_string())
    [foo.bar]
    x = 1
    """
    return Table(Container(), Trivia(), False, is_super_table)


def table(ax: Axes, data: DataFrame | Series, **kwargs) -> Table:
    """
    Helper function to convert DataFrame and Series to matplotlib.table.

    This method provides an easy way to visualize tabular data within a Matplotlib
    figure. It automatically extracts index and column labels from the DataFrame
    or Series, unless explicitly specified. This function is particularly useful
    when displaying summary tables alongside other plots or when creating static
    reports. It utilizes the `matplotlib.pyplot.table` backend and allows
    customization through various styling options available in Matplotlib.

    Parameters
    ----------
    ax : Matplotlib axes object
        The axes on which to draw the table.
    data : DataFrame or Series
        Data for table contents.
    **kwargs
        Keyword arguments to be passed to matplotlib.table.table.
        If `rowLabels` or `colLabels` is not specified, data index or column
        names will be used.

    Returns
    -------
    matplotlib table object
        The created table as a matplotlib Table object.

    See Also
    --------
    DataFrame.plot : Make plots of DataFrame using matplotlib.
    matplotlib.pyplot.table : Create a table from data in a Matplotlib plot.

    Examples
    --------

    .. plot::
            :context: close-figs

            >>> import matplotlib.pyplot as plt
            >>> df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
            >>> fig, ax = plt.subplots()
            >>> ax.axis("off")
            (np.float64(0.0), np.float64(1.0), np.float64(0.0), np.float64(1.0))
            >>> table = pd.plotting.table(
            ...     ax, df, loc="center", cellLoc="center", colWidths=[0.2, 0.2]
            ... )
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.table(
        ax=ax, data=data, rowLabels=None, colLabels=None, **kwargs
    )


def table(
    ax, data: DataFrame | Series, rowLabels=None, colLabels=None, **kwargs
) -> Table:
    if isinstance(data, ABCSeries):
        data = data.to_frame()
    elif isinstance(data, ABCDataFrame):
        pass
    else:
        raise ValueError("Input data must be DataFrame or Series")

    if rowLabels is None:
        rowLabels = data.index

    if colLabels is None:
        colLabels = data.columns

    cellText = data.values

    # error: Argument "cellText" to "table" has incompatible type "ndarray[Any,
    # Any]"; expected "Sequence[Sequence[str]] | None"
    return mpl.table.table(
        ax,
        cellText=cellText,  # type: ignore[arg-type]
        rowLabels=rowLabels,
        colLabels=colLabels,
        **kwargs,
    )


def table(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    tbodyLines = None

    # should have at least two lines
    if startLine + 2 > endLine:
        return False

    nextLine = startLine + 1

    if state.sCount[nextLine] < state.blkIndent:
        return False

    if state.is_code_block(nextLine):
        return False

    # first character of the second line should be '|', '-', ':',
    # and no other characters are allowed but spaces;
    # basically, this is the equivalent of /^[-:|][-:|\s]*$/ regexp

    pos = state.bMarks[nextLine] + state.tShift[nextLine]
    if pos >= state.eMarks[nextLine]:
        return False
    first_ch = state.src[pos]
    pos += 1
    if first_ch not in ("|", "-", ":"):
        return False

    if pos >= state.eMarks[nextLine]:
        return False
    second_ch = state.src[pos]
    pos += 1
    if second_ch not in ("|", "-", ":") and not isStrSpace(second_ch):
        return False

    # if first character is '-', then second character must not be a space
    # (due to parsing ambiguity with list)
    if first_ch == "-" and isStrSpace(second_ch):
        return False

    while pos < state.eMarks[nextLine]:
        ch = state.src[pos]

        if ch not in ("|", "-", ":") and not isStrSpace(ch):
            return False

        pos += 1

    lineText = getLine(state, startLine + 1)

    columns = lineText.split("|")
    aligns = []
    for i in range(len(columns)):
        t = columns[i].strip()
        if not t:
            # allow empty columns before and after table, but not in between columns;
            # e.g. allow ` |---| `, disallow ` ---||--- `
            if i == 0 or i == len(columns) - 1:
                continue
            else:
                return False

        if not headerLineRe.search(t):
            return False
        if charStrAt(t, len(t) - 1) == ":":
            aligns.append("center" if charStrAt(t, 0) == ":" else "right")
        elif charStrAt(t, 0) == ":":
            aligns.append("left")
        else:
            aligns.append("")

    lineText = getLine(state, startLine).strip()
    if "|" not in lineText:
        return False
    if state.is_code_block(startLine):
        return False
    columns = escapedSplit(lineText)
    if columns and columns[0] == "":
        columns.pop(0)
    if columns and columns[-1] == "":
        columns.pop()

    # header row will define an amount of columns in the entire table,
    # and align row should be exactly the same (the rest of the rows can differ)
    columnCount = len(columns)
    if columnCount == 0 or columnCount != len(aligns):
        return False

    if silent:
        return True

    oldParentType = state.parentType
    state.parentType = "table"

    # use 'blockquote' lists for termination because it's
    # the most similar to tables
    terminatorRules = state.md.block.ruler.getRules("blockquote")

    token = state.push("table_open", "table", 1)
    token.map = tableLines = [startLine, 0]

    token = state.push("thead_open", "thead", 1)
    token.map = [startLine, startLine + 1]

    token = state.push("tr_open", "tr", 1)
    token.map = [startLine, startLine + 1]

    for i in range(len(columns)):
        token = state.push("th_open", "th", 1)
        if aligns[i]:
            token.attrs = {"style": "text-align:" + aligns[i]}

        token = state.push("inline", "", 0)
        # note in markdown-it this map was removed in v12.0.0 however, we keep it,
        # since it is helpful to propagate to children tokens
        token.map = [startLine, startLine + 1]
        token.content = columns[i].strip()
        token.children = []

        token = state.push("th_close", "th", -1)

    token = state.push("tr_close", "tr", -1)
    token = state.push("thead_close", "thead", -1)

    autocompleted_cells = 0
    nextLine = startLine + 2
    while nextLine < endLine:
        if state.sCount[nextLine] < state.blkIndent:
            break

        terminate = False
        for i in range(len(terminatorRules)):
            if terminatorRules[i](state, nextLine, endLine, True):
                terminate = True
                break

        if terminate:
            break
        lineText = getLine(state, nextLine).strip()
        if not lineText:
            break
        if state.is_code_block(nextLine):
            break
        columns = escapedSplit(lineText)
        if columns and columns[0] == "":
            columns.pop(0)
        if columns and columns[-1] == "":
            columns.pop()

        # note: autocomplete count can be negative if user specifies more columns than header,
        # but that does not affect intended use (which is limiting expansion)
        autocompleted_cells += columnCount - len(columns)
        if autocompleted_cells > MAX_AUTOCOMPLETED_CELLS:
            break

        if nextLine == startLine + 2:
            token = state.push("tbody_open", "tbody", 1)
            token.map = tbodyLines = [startLine + 2, 0]

        token = state.push("tr_open", "tr", 1)
        token.map = [nextLine, nextLine + 1]

        for i in range(columnCount):
            token = state.push("td_open", "td", 1)
            if aligns[i]:
                token.attrs = {"style": "text-align:" + aligns[i]}

            token = state.push("inline", "", 0)
            # note in markdown-it this map was removed in v12.0.0 however, we keep it,
            # since it is helpful to propagate to children tokens
            token.map = [nextLine, nextLine + 1]
            try:
                token.content = columns[i].strip() if columns[i] else ""
            except IndexError:
                token.content = ""
            token.children = []

            token = state.push("td_close", "td", -1)

        token = state.push("tr_close", "tr", -1)

        nextLine += 1

    if tbodyLines:
        token = state.push("tbody_close", "tbody", -1)
        tbodyLines[1] = nextLine

    token = state.push("table_close", "table", -1)

    tableLines[1] = nextLine
    state.parentType = oldParentType
    state.line = nextLine
    return True

