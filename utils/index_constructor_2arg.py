
def index_constructor_2arg(context, builder, sig, args):
    (data, hashmap, parent) = args
    index = cgutils.create_struct_proxy(sig.return_type)(context, builder)

    index.data = data
    index.hashmap = hashmap
    index.parent = parent
    return impl_ret_borrowed(context, builder, sig.return_type, index._getvalue())

