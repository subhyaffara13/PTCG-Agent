
def pdseries_constructor_with_name(context, builder, sig, args):
    data, index, name = args
    series = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    series.index = index
    series.values = data
    series.name = name
    return impl_ret_borrowed(context, builder, sig.return_type, series._getvalue())

