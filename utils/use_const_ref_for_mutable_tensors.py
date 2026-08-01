
def use_const_ref_for_mutable_tensors() -> bool:
    if _locals.use_const_ref_for_mutable_tensors is None:
        raise AssertionError(
            "need to initialize local.use_const_ref_for_mutable_tensors with "
            "local.parametrize"
        )
    return _locals.use_const_ref_for_mutable_tensors

