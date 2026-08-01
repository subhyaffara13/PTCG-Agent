
def use_ilistref_for_tensor_lists() -> bool:
    if _locals.use_ilistref_for_tensor_lists is None:
        raise AssertionError(
            "need to initialize local.use_ilistref_for_tensor_lists with local.parametrize"
        )
    return _locals.use_ilistref_for_tensor_lists

