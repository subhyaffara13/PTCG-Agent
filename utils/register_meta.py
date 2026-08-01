
def register_meta(op) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def wrapper(fn):
        fn = _convert_out_params(fn)

        def register(op):
            _add_op_to_registry(meta_table, op, fn)

        pytree.tree_map_(register, op)
        return fn

    return wrapper

