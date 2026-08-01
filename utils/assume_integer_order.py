
def assume_integer_order(fn):
    @wraps(fn)
    def g(self, nu, z):
        if nu.is_integer:
            return fn(self, nu, z)
    return g

