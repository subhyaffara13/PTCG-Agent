
def namespace_path_split(path):
    """Split the namespace path into a pair (head, tail).

    Tail will be the last namespace path component and head will
    be everything leading up to that in the path. This is similar to
    os.path.split.

    :param path: (String) A namespace path.
    :returns: (String, String) A tuple where the first component is the base
              path and the second is the last path component.
    """
    return tuple(path.rsplit(".", 1))

