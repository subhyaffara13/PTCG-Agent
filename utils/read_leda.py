
def read_leda(path, encoding="UTF-8"):
    """Read graph in LEDA format from path.

    Parameters
    ----------
    path : file or string
       Filename or file handle to read.
       Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    G : NetworkX graph

    Examples
    --------
    >>> G = nx.read_leda("file.leda")  # doctest: +SKIP

    References
    ----------
    .. [1] http://www.algorithmic-solutions.info/leda_guide/graphs/leda_native_graph_fileformat.html
    """
    lines = (line.decode(encoding) for line in path)
    G = parse_leda(lines)
    return G

