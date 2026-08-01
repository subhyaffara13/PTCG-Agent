
def index_constructor_1arg(context, builder, sig, args):
    from numba.typed import Dict

    key_type = sig.return_type.dtype
    value_type = types.intp

    def index_impl(data):
        return Index(data, Dict.empty(key_type, value_type))

    return context.compile_internal(builder, index_impl, sig, args)

