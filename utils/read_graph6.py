
def read_graph6(path):
    """Read simple undirected graphs in graph6 format from path.

    Parameters
    ----------
    path : file or string
       Filename or file handle to read.
       Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    G : Graph or list of Graphs
       If the file contains multiple lines then a list of graphs is returned

    Raises
    ------
    NetworkXError
        If the string is unable to be parsed in graph6 format

    Examples
    --------
    You can read a graph6 file by giving the path to the file::

        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(delete=False) as f:
        ...     _ = f.write(b">>graph6<<A_\\n")
        ...     _ = f.seek(0)
        ...     G = nx.read_graph6(f.name)
        >>> list(G.edges())
        [(0, 1)]

    You can also read a graph6 file by giving an open file-like object::

        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile() as f:
        ...     _ = f.write(b">>graph6<<A_\\n")
        ...     _ = f.seek(0)
        ...     G = nx.read_graph6(f)
        >>> list(G.edges())
        [(0, 1)]

    See Also
    --------
    from_graph6_bytes, write_graph6

    References
    ----------
    .. [1] Graph6 specification
           <http://users.cecs.anu.edu.au/~bdm/data/formats.html>

    """
    glist = []
    for line in path:
        line = line.strip()
        if not len(line):
            continue
        glist.append(from_graph6_bytes(line))
    if len(glist) == 1:
        return glist[0]
    else:
        return glist

