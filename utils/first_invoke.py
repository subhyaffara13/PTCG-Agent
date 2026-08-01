
def first_invoke(func1, func2):
    """
    Return a function that when invoked will invoke func1 without
    any parameters (for its side effect) and then invoke func2
    with whatever parameters were passed, returning its result.
    """

    def wrapper(*args, **kwargs):
        func1()
        return func2(*args, **kwargs)

    return wrapper

