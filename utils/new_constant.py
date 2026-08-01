
def new_constant(fill_value):
    def _new_constant(
        x, size, *, dtype=None, layout=None, device=None, pin_memory=None
    ):
        assert isinstance(size, (list, tuple))
        assert_nyi(not pin_memory, "pin_memory")
        assert_nyi(layout in (None, torch.strided), f"layout={layout}")
        # pyrefly: ignore [bad-argument-type]
        dtype = decode_dtype(dtype) or x.get_dtype()
        device = device or x.get_device()
        size = [sympy.Integer(s) for s in size]
        return _full(fill_value, decode_device(device), dtype, size)

    return _new_constant

