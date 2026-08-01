
def auto_functionalized_fake(
    mode,
    _mutable_op: OpOverload,
    **kwargs: Any,
) -> tuple[Any, tuple[Tensor, ...]]:
    with mode:
        result = auto_functionalized_dense(
            _mutable_op, _only_clone_these_tensors=None, **kwargs
        )
        return result

