
def uncurry(func):
    def uncurry_rl(args):
        return func(*args)
    return uncurry_rl

