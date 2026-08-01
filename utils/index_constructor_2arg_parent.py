
def index_constructor_2arg_parent(context, builder, sig, args):
    # Basically same as index_constructor_1arg, but also lets you specify the
    # parent object
    (data, hashmap) = args
    index = cgutils.create_struct_proxy(sig.return_type)(context, builder)

    index.data = data
    index.hashmap = hashmap
    return impl_ret_borrowed(context, builder, sig.return_type, index._getvalue())

