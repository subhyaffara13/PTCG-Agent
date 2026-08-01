
def simple_scan(init, xs):
    def combine_fn(carry, x):
        result = carry @ x + x
        return result, carry.clone()

    return torch._higher_order_ops.scan(combine_fn, init, xs)

