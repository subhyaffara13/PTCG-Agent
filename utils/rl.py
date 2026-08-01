
def rl(x):
    if x.args and not isinstance(x.args[0], Integer):
        return Basic2(*x.args)
    return x

