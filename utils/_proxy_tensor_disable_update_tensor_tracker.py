
def _proxy_tensor_disable_update_tensor_tracker() -> Generator[None, None, None]:
    """
    NOTE "Do not clobber inplace ops"
    By default tensor_tracker is updated every time.
    This leads to chaining every operation by the FakeTensor.
    For example for mutable ops if we have several consecutive mutable operations:

    def f(x, y, z):
        x.copy_(y)
        x.copy_(z)
        return x

    Default graph result:
    def f_graph(x, y, z)
        x_1 = x.copy_(y)
        x_2 = x_1.copy_(z)
        return x_2

    This chaining simplifies the fx passes and helps to prevent the reordering.
    But in some cases, we want those nodes to be disconnected.
    E.g. in case of splitting joint graph into forward and backward.
    If first inplace op happened in forward, second in backward,
    we want them after split to be properly placed.

    Enabling this context manager for copy_ will result in:
    def f_graph_2(x, y, z):
        x_1 = x.copy_(y)
        x_2 = x.copy_(z)
        return x

    Results of copy_ x1 and x2 will have empty users in the graph.
    The reason why this behavior is not enabled for all inplace ops is that
    some fx passes (e.g. fx quantization) rely on chaining inplace ops like add_
    in their fusions passes.
    We could revisit enabling this logic for all inplace ops in future.
    """
    orig_value = _disable_update_tensor_tracker_tls.value
    _disable_update_tensor_tracker_tls.value = True
    try:
        yield
    finally:
        _disable_update_tensor_tracker_tls.value = orig_value

