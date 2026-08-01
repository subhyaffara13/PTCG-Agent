
def tensor_constructor(fill_value):
    # torch.zeros, torch.ones, etc
    def inner(
        *size,
        names=None,
        dtype=None,
        device=None,
        layout=None,
        pin_memory=False,
        memory_format=None,
    ):
        assert_nyi(names is None, "named tensors")
        assert_nyi(layout in (None, torch.strided), f"layout={layout}")
        assert_nyi(not pin_memory, "pin_memory")
        device = decode_device(device)
        dtype = dtype or torch.get_default_dtype()
        if len(size) == 1 and isinstance(size[0], (list, tuple, torch.Size)):
            size = tuple(size[0])
        # See https://github.com/pytorch/pytorch/issues/118102
        # All sizes at lowering time should be sympy.Symbol, not SymInt!
        for s in size:
            assert not isinstance(s, torch.SymInt)
        size = [sympy.expand(s) for s in size]
        return _full(fill_value, device, dtype, size)

    return inner

