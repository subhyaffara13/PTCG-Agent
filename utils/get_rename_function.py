
def get_rename_function(mapper):
    """
    Returns a function that will map names/labels, dependent if mapper
    is a dict, Series or just a function.
    """

    def f(x):
        if x in mapper:
            return mapper[x]
        else:
            return x

    return f if isinstance(mapper, (abc.Mapping, ABCSeries)) else mapper

