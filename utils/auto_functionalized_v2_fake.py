
def auto_functionalized_v2_fake(
    mode,
    _mutable_op: _MutableOpType,
    **kwargs: dict[str, Any],
) -> tuple[Any, tuple[Tensor, ...]]:
    with mode:
        result = auto_functionalized_v2_dense(
            _mutable_op, _only_clone_these_bases=None, **kwargs
        )
        return result

