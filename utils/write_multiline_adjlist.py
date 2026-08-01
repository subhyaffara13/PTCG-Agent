
def write_multiline_adjlist(G, path, delimiter=" ", comments="#", encoding="utf-8"):
    """Write the graph G in multiline adjacency list format to path

    Parameters
    ----------
    G : NetworkX graph

    path : string or file
       Filename or file handle to write to.
       Filenames ending in .gz or .bz2 will be compressed.

    comments : string, optional
       Marker for comment lines

    delimiter : string, optional
       Separator for node labels

    encoding : string, optional
       Text encoding.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.write_multiline_adjlist(G, "test.multi_adjlist")

    The path can be a file handle or a string with the name of the file. If a
    file handle is provided, it has to be opened in 'wb' mode.

    >>> fh = open("test.multi_adjlist2", "wb")
    >>> nx.write_multiline_adjlist(G, fh)

    Filenames ending in .gz or .bz2 will be compressed.

    >>> nx.write_multiline_adjlist(G, "test.multi_adjlist.gz")

    See Also
    --------
    read_multiline_adjlist
    """
    import sys
    import time

    pargs = comments + " ".join(sys.argv)
    header = (
        f"{pargs}\n"
        + comments
        + f" GMT {time.asctime(time.gmtime())}\n"
        + comments
        + f" {G.name}\n"
    )
    path.write(header.encode(encoding))

    for multiline in generate_multiline_adjlist(G, delimiter):
        multiline += "\n"
        path.write(multiline.encode(encoding))

