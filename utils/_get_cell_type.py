
def _get_cell_type():
    def f(x=None):
        return lambda: x
    return type(f().__closure__[0])

