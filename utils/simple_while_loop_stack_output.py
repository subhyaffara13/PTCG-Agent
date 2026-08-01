
def simple_while_loop_stack_output(iter_t, x):
    def cond_fn(iter_t, x):
        return iter_t > 0

    def body_fn(iter_t, x):
        return iter_t - 1, x.cos()

    return torch._higher_order_ops.while_loop_stack_output(
        cond_fn, body_fn, (iter_t, x), tuple()
    )

