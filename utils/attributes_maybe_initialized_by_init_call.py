
def attributes_maybe_initialized_by_init_call(op: Call) -> set[str]:
    """Calculate attributes that may be initialized by a super().__init__ call."""
    self_type = op.fn.sig.args[0].type
    assert isinstance(self_type, RInstance), self_type
    cl = self_type.class_ir
    return attributes_initialized_by_init_call(op) | cl._sometimes_initialized_attrs

