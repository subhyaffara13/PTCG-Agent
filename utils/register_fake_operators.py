
def register_fake_operators():
    @torch.library.register_fake("_TorchScriptTesting::takes_foo_python_meta")
    def fake_takes_foo(foo, z):
        return foo.add_tensor(z)

    @torch.library.register_fake("_TorchScriptTesting::queue_pop")
    def fake_queue_pop(tq):
        return tq.pop()

    @torch.library.register_fake("_TorchScriptTesting::queue_push")
    def fake_queue_push(tq, x):
        return tq.push(x)

    torch.library.register_autocast(
        "_TorchScriptTesting::queue_push", "cpu", torch.float32
    )
    torch.library.register_autocast(
        "_TorchScriptTesting::queue_push", "cuda", torch.float32
    )

    torch.library.register_autocast(
        "_TorchScriptTesting::queue_pop", "cpu", torch.float32
    )
    torch.library.register_autocast(
        "_TorchScriptTesting::queue_pop", "cuda", torch.float32
    )

    @torch.library.register_fake("_TorchScriptTesting::queue_size")
    def fake_queue_size(tq):
        return tq.size()

    def meta_takes_foo_list_return(foo, x):
        a = foo.add_tensor(x)
        b = foo.add_tensor(a)
        c = foo.add_tensor(b)
        return [a, b, c]

    def meta_takes_foo_tuple_return(foo, x):
        a = foo.add_tensor(x)
        b = foo.add_tensor(a)
        return (a, b)

    @torch.library.register_fake("_TorchScriptTesting::takes_foo_tensor_return")
    def meta_takes_foo_tensor_return(foo, x):
        # This implementation deliberately creates unbacked symint for testing
        ctx = torch.library.get_ctx()
        fake_shape = [ctx.new_dynamic_size() for _ in range(2)]
        return torch.empty(fake_shape, dtype=torch.int, device="cpu")

    torch.ops._TorchScriptTesting.takes_foo_list_return.default.py_impl(
        torch._C.DispatchKey.Meta
    )(meta_takes_foo_list_return)

    torch.ops._TorchScriptTesting.takes_foo_tuple_return.default.py_impl(
        torch._C.DispatchKey.Meta
    )(meta_takes_foo_tuple_return)

    torch.ops._TorchScriptTesting.takes_foo.default.py_impl(torch._C.DispatchKey.Meta)(
        # make signature match original cpp implementation to support kwargs
        lambda foo, x: foo.add_tensor(x)
    )

