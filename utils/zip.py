
def zip(*args):
    """Ensure each argument to zip has the same length. Also make sure a list is
    returned for python 2/3 compatibility.
    """

    if len(set(len(a) for a in args)) != 1:
        raise UnequalZipLengthsError(*args)
    return list(_zip(*args))

