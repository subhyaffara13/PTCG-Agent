
def num_pos_args(sigspec):
    """ Return the number of positional arguments.  ``f(x, y=1)`` has 1"""
    return sum(1 for x in sigspec.parameters.values()
               if x.kind == x.POSITIONAL_OR_KEYWORD
               and x.default is x.empty)

