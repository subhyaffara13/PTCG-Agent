
def attributes_initialized_by_init_call(op: Call) -> set[str]:
    """Calculate attributes that are always initialized by a super().__init__ call."""
    self_type = op.fn.sig.args[0].type
    assert isinstance(self_type, RInstance), self_type
    cl = self_type.class_ir
    return {a for base in cl.mro for a in base.attributes if base.is_always_defined(a)}

