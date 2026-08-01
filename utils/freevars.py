
def freevars(func):
    """get objects defined in enclosing code that are referred to by func

    returns a dict of {name:object}"""
    if ismethod(func): func = func.__func__
    if isfunction(func):
        closures = func.__closure__ or ()
        func = func.__code__.co_freevars # get freevars
    else:
        return {}

    def get_cell_contents():
        for name, c in zip(func, closures):
            try:
                cell_contents = c.cell_contents
            except ValueError: # cell is empty
                continue
            yield name, c.cell_contents

    return dict(get_cell_contents())

